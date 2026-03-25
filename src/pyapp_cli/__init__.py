import typer

from .generator import ProjectGenerator
from .logger import Logger
from .schemas import Framework, PackageManager, SourceFolder
from .questions import Questions

app = typer.Typer()
project_generator = ProjectGenerator(logger=Logger(), questions=Questions())


@app.command()
def init(
    verbose: bool = False,
    project_path: str | None = None,
    package_manager: PackageManager | None = None,
    python_version: str | None = None,
    source_folder: SourceFolder | None = None,
    framework: Framework | None = None,
    libraries: list[str] | None = None,
) -> None:
    project_generator.init(
        verbose=verbose,
        project_path=project_path,
        package_manager=package_manager,
        python_version=python_version,
        source_folder=source_folder,
        framework=framework,
        libraries=libraries,
    )


@app.command()
def dummy() -> None:
    print("Hello, World!")


def main() -> None:
    app()
