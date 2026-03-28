import importlib.metadata
from typing import Literal

from colorama import Fore

from .logger import Logger
from .project_generator import ProjectGenerator
from .schemas import Framework, PackageManager, SourceFolder

VENV_DIR = ".venv"


class PyAppCLI:
    # frameworks without built-in CLI for scaffolding the project
    _no_cli_frameworks: set[Framework] = set(["fastapi", "flask"])

    _logger: Logger
    _project_generator: ProjectGenerator

    def __init__(self, logger: Logger, project_generator: ProjectGenerator) -> None:
        self._logger = logger
        self._project_generator = project_generator

    def init(
        self,
        verbose: bool,
        project_path: str | None,
        package_manager: PackageManager | None,
        python_version: str | None,
        source_folder: SourceFolder | None,
        framework: Framework | None,
        libraries: str | None,
        no_libraries: Literal[True] | None,
    ) -> None:
        self._project_generator.generate(
            verbose=verbose,
            project_path=project_path,
            package_manager=package_manager,
            python_version=python_version,
            source_folder=source_folder,
            framework=framework,
            libraries=libraries,
            no_libraries=no_libraries,
        )

    def get_version(self) -> None:
        lib_version = importlib.metadata.version("pyapp-cli")
        self._logger.log(f"PyApp CLI version: {Fore.CYAN + lib_version}")
