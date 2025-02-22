import functools
import importlib
import subprocess
import sys
import traceback
from typing import Callable, List, Mapping, TypedDict

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import (
    darn_to_string,
    get_git_repo,
    get_relative_project_path,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import get_sca_prime_shadow_results, start_sca_prime_shadow
from gable.openapi import SourceType, StructuredDataAssetResourceName
from loguru import logger

SwiftConfig = TypedDict(
    "SwiftConfig",
    {
        "project_root": click.Path,
        "annotation": str,
        "debug": click.Option,
    },
)


class SwiftAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.swift

    def click_options_decorator(self) -> Callable:
        def decorator(func):
            @click.option(
                "--project_root",
                help="The directory location of the Swift project that will be analyzed.",
                type=click.Path(exists=True),
                required=True,
            )
            @click.option(
                "--annotation",
                help="Annotation name that will be used for asset detection, can include multiple entries e.g. --annotation <a> --annotation <b>",
                type=str,
                multiple=True,
                required=False,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(SwiftConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        typed_config = SwiftConfig(**config)
        if not typed_config["project_root"]:
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} Missing required options for Swift project registration. --project-root is required. You can use the --help option for more details.",
                param_type="option",
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        try:
            typed_config = SwiftConfig(**config)
            project_root = config["project_root"]

            annotations = []
            if "annotation" in config:
                annotations = config["annotation"]

            semgrep_bin_path = self.install_semgrep()

            sca_prime_future = start_sca_prime_shadow(
                client=client,
                project_root=project_root,
                annotations=annotations,
                sca_debug=("debug" in config),
                semgrep_bin_path=semgrep_bin_path,
            )
            results = get_sca_prime_shadow_results(
                sca_prime_future,
                client,
                project_root,
                post_metrics=False,
            )

            git_ssh_repo = get_git_repo(str(typed_config["project_root"]))
            project_name, relative_swift_project_root = get_relative_project_path(
                str(typed_config["project_root"])
            )
            # WARNING: we do not yet support DARN creation in sca-prime, meaning the `data_source` is
            # subject to change and is in no way robust.
            data_source = (
                f"git@{git_ssh_repo}:{relative_swift_project_root}:{project_name}"
            )
            assets = [
                ExtractedAsset(
                    darn=StructuredDataAssetResourceName(
                        source_type=SourceType.swift,
                        data_source=data_source,
                        path=event_name,
                    ),
                    fields=[
                        field
                        for field in map(
                            ExtractedAsset.safe_parse_field, event_schema["fields"]
                        )
                        if field is not None
                    ],
                    dataProfileMapping=None,
                )
                for event_name, event_schema in {**results}.items()
            ]

        except Exception as e:
            traceback.print_exc()
            raise click.ClickException(
                f"{EMOJI.RED_X.value} FAILURE: {e}",
            )

        result = ""
        for asset in assets:
            finding = ""
            darn_str = darn_to_string(asset.darn)
            finding += f"Asset Schema: [\n"

            for field in asset.fields:
                finding += f"  {field.json()},\n"

            finding += f"]\n"
            finding += f"Located at {darn_str}\n"
            result += finding

        logger.info(result)
        return assets

    def checked_when_registered(self) -> bool:
        return False

    def install_semgrep(self) -> str:
        return "".join(self._pip_install("semgrep", "1.90.0"))

    def _pip_install(self, package, exact_version, import_name=None) -> str:
        """
        Install a package using pip if it's not already installed
        """
        try:
            return importlib.import_module(import_name or package).__path__[0]
        except ImportError:
            try:
                subprocess.run(
                    [
                        # sys.executable is the path to the current python interpreter so we know
                        # we're installing the package in the same environment
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        f"{package}=={exact_version}",
                    ],
                    check=True,
                )
                return importlib.import_module(import_name or package).__path__[0]

            except Exception as e:
                raise click.ClickException(
                    f"Error installing {package}: {e}",
                )
