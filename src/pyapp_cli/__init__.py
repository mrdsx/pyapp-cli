from typing import Literal

import typer

from .libraries import LibrariesGenerator
from .logger import Logger
from .prompt_handler import PromptHandler
from .pyapp_cli import PyAppCLI
from .schemas import Framework, PackageManager, SourceFolder

app = typer.Typer()
prompts = PromptHandler(
    libraries_generator=LibrariesGenerator(),
)

cli = PyAppCLI(
    logger=Logger(),
    prompt_handler=prompts,
)


@app.command()
def init(
    verbose: bool = False,
    project_path: str | None = None,
    package_manager: PackageManager | None = None,
    python_version: str | None = None,
    source_folder: SourceFolder | None = None,
    framework: Framework | None = None,
    libraries: str | None = None,
    no_libraries: Literal[True] | None = None,
) -> None:
    cli.init(
        verbose=verbose,
        project_path=project_path,
        package_manager=package_manager,
        python_version=python_version,
        source_folder=source_folder,
        framework=framework,
        libraries=libraries,
        no_libraries=no_libraries,
    )


@app.command()
def version() -> None:
    cli.get_version()


def main() -> None:
    app()
