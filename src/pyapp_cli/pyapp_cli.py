import importlib.metadata
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

from colorama import Fore
from pydantic import ValidationError

from .logger import Logger
from .questions import Questions
from .schemas import Answers, Framework, PackageManager, SourceFolder
from .templates import templates

VENV_DIR = ".venv"


class PyAppCLI:
    # frameworks without built-in CLI for scaffolding the project
    _no_cli_frameworks: set[Framework] = set(["fastapi", "flask"])
    _stdout: int | None
    _logger: Logger
    _questions: Questions

    def __init__(self, logger: Logger, questions: Questions) -> None:
        self._logger = logger
        self._questions = questions

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
        self._stdout = None if verbose else subprocess.DEVNULL
        self._logger.verbose = verbose
        self._logger.debug(f"stdout: {self._stdout}")
        self._logger.debug(f"Verbose logging: {self._logger.verbose}")

        try:
            raw_answers = self._questions.prompt(
                project_path=project_path,
                package_manager=package_manager,
                python_version=python_version,
                source_folder=source_folder,
                framework=framework,
                libraries=libraries,
                no_libraries=no_libraries,
            )
            answers = Answers(**raw_answers)
        except (TypeError, ValidationError) as error:
            self._logger.error("Invalid project params")
            self._logger.debug(f"Error: {error}")
            exit(1)
        except KeyboardInterrupt:
            self._logger.error("Project setup has been interrupted")
            exit(1)

        if answers.package_manager == "pip":
            self._ensure_pip_installation()
        elif answers.package_manager == "poetry":
            self._ensure_poetry_installation()
        elif answers.package_manager == "uv":
            self._ensure_uv_installation()

        escaped_path = self._escape_project_path(answers.project_path)
        self._create_project_folder(escaped_path, answers.source_folder)

        if answers.framework is None or answers.framework in self._no_cli_frameworks:
            self._create_main_file(answers.source_folder, answers.framework)

        dependencies = answers.libraries
        if answers.framework is not None:
            dependencies.append(answers.framework)
        self._logger.debug(f"Selected dependencies: {dependencies}")

        self._logger.debug(f"Package manager: {answers.package_manager}")
        if answers.package_manager == "pip":
            self._pip_setup_project(dependencies)
        elif answers.package_manager == "poetry":
            self._poetry_setup_project(dependencies, answers.python_version)
        elif answers.package_manager == "uv":
            self._uv_setup_project(dependencies, answers.python_version)

        if answers.framework == "django":
            self._django_setup_project(answers.source_folder)

        self._logger.success("Finished! Enjoy the project :)")

    def get_version(self) -> None:
        lib_version = importlib.metadata.version("pyapp-cli")
        self._logger.log(f"PyApp CLI version: {Fore.CYAN + lib_version}")

    def _escape_project_path(self, path: str) -> str:
        result = path
        if path.strip() == "":
            result = "."

        self._logger.debug(f"Escaped project path with result '{result}'")
        return result

    def _get_python_executable_path(self) -> str:
        if sys.platform == "win32":
            executable = os.path.abspath(
                os.path.join(VENV_DIR, "Scripts", "python.exe")
            )
        else:
            executable = os.path.abspath(os.path.join(VENV_DIR, "bin", "python3"))

        self._logger.debug(f"Current Python executable: {executable}")
        return executable

    def _missing_dependency_message(self, dependency: str) -> str:
        return (
            f"Can't detect installed {dependency}.\n"
            f"Ensure {dependency} is installed and then run the script again."
        )

    def _create_project_folder(
        self, project_path: str, source_folder: SourceFolder
    ) -> None:
        self._logger.debug(f"Creating folder at '{project_path}'...")
        Path(project_path).mkdir(exist_ok=True)
        if source_folder != "root":
            Path(project_path, source_folder).mkdir(exist_ok=True)
            self._logger.debug(
                f"Created source folder at '{os.path.join(project_path, source_folder)}'"
            )
        os.chdir(project_path)
        self._logger.log(f"Created folder '{project_path}'")

    def _ensure_pip_installation(self) -> None:
        pip_exists = shutil.which("pip") is not None
        if pip_exists:
            self._logger.success("Detected pip")
        else:
            self._logger.error(self._missing_dependency_message("pip"))
            exit(127)

    def _ensure_poetry_installation(self) -> None:
        poetry_exists = shutil.which("poetry") is not None
        if poetry_exists:
            self._logger.success("Detected Poetry")
        else:
            self._logger.error(self._missing_dependency_message("Poetry"))
            exit(127)

    def _ensure_uv_installation(self) -> None:
        uv_exists = shutil.which("uv") is not None
        if uv_exists:
            self._logger.success("Detected uv")
        else:
            self._logger.error(self._missing_dependency_message("uv"))
            exit(127)

    def _create_main_file(
        self, source_folder: SourceFolder, framework: Framework | None
    ) -> None:
        python_file = None
        if source_folder == "root":
            python_file = Path("main.py")
        else:
            python_file = Path(source_folder, "main.py")
        python_file.parent.mkdir(parents=True, exist_ok=True)
        self._logger.log("Added main.py")

        project_template = templates.get(framework or "")
        with open(python_file, "w") as f:
            if project_template is not None:
                f.write(project_template)
                self._logger.debug(f"Created {framework} template")

    def _pip_setup_project(self, dependencies: list[str]) -> None:
        self._logger.log("Creating virtual environment...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "venv",
                os.path.join(VENV_DIR),
            ],
            stdout=self._stdout,
            stderr=self._stdout,
        )

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            python_executable = self._get_python_executable_path()
            subprocess.check_call(
                [python_executable, "-m", "pip", "install", *dependencies],
            )
            result = subprocess.run(
                [python_executable, "-m", "pip", "freeze"],
                check=True,
                capture_output=True,
                text=True,
            )
            with open("requirements.txt", "w") as f:
                f.write(result.stdout)
            self._logger.success("Saved dependencies to requirements.txt")

    def _poetry_setup_project(
        self, dependencies: list[str], python_version: str
    ) -> None:
        subprocess.check_call(
            ["poetry", "init", "-n", f"--python=>={python_version}"],
            stdout=self._stdout,
            stderr=self._stdout,
        )
        self._logger.log("Initialized poetry project")

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            custom_env = os.environ.copy()
            custom_env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
            custom_env["VIRTUAL_ENV"] = os.path.abspath(VENV_DIR)
            self._logger.debug(f"Virtual environment: {custom_env['VIRTUAL_ENV']}")
            subprocess.check_call(
                [
                    "poetry",
                    "add",
                    *dependencies,
                ],
                env=custom_env,
            )

    def _uv_setup_project(self, dependencies: list[str], python_version: str) -> None:
        subprocess.check_call(
            [
                "uv",
                "init",
                "--bare",
                "--no-workspace",
                "--python",
                f"{python_version}",
            ],
            stdout=self._stdout,
            stderr=self._stdout,
        )
        with open(".python-version", "w") as f:
            f.write(python_version)
        self._logger.log("Initialized uv project")

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            subprocess.check_call(
                [
                    "uv",
                    "add",
                    *dependencies,
                ],
            )

    def _django_setup_project(self, source_folder: SourceFolder) -> None:
        python_executable = self._get_python_executable_path()
        django_util = [python_executable, "-m", "django"]

        if source_folder != "root":
            os.chdir(source_folder)
            self._logger.debug(f"Set working directory to '{source_folder}'...")

        subprocess.check_call(
            [*django_util, "startproject", "mysite", "."],
        )
        self._logger.log("Initialized Django project")
