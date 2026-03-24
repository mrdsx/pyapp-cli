import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Literal

import fire
from InquirerPy import prompt

from logger import Logger
from questions import questions
from schemas import Answers

venv_dir = ".venv"


class ProjectGenerator:
    # frameworks without built-in CLI for scaffolding the project
    _framework_packages = set(["FastAPI", "Flask"])
    _templates_dir = os.path.abspath("templates")

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def init(self):
        raw_answers = prompt(questions)
        answers = Answers.model_validate(raw_answers)

        self._create_project_folder(answers.project_path, answers.source_folder)

        if answers.package_manager == "pip":
            self._ensure_pip_installation()
        elif answers.package_manager == "poetry":
            self._ensure_poetry_installation()
        elif answers.package_manager == "uv":
            self._ensure_uv_installation()

        if answers.framework == "None" or answers.framework in self._framework_packages:
            self._create_main_file(answers.source_folder, answers.framework)

        dependencies = answers.libraries
        if answers.framework != "None":
            dependencies.append(self._framework_id(answers.framework))

        if answers.package_manager == "pip":
            self._pip_setup_project(dependencies)
        elif answers.package_manager == "poetry":
            self._poetry_setup_project(dependencies)
        elif answers.package_manager == "uv":
            self._uv_setup_project(dependencies, answers.python_version)

        if answers.framework == "Django":
            self._django_setup_project(answers.package_manager, answers.source_folder)

        self._logger.success("Finished! Enjoy the project :)")

    def _framework_id(self, framework: str) -> str:
        return framework.lower()

    def _missing_dependency_message(self, dependency: str) -> str:
        return (
            f"Can't detect installed {dependency}.\n"
            f"Ensure {dependency} is installed and then run the script again."
        )

    def _create_project_folder(self, project_path: str, source_folder: str) -> None:
        Path(project_path).mkdir(exist_ok=True)
        if source_folder != "root":
            Path(project_path, source_folder).mkdir(exist_ok=True)
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

    def _create_main_file(self, source_folder: str, framework: str) -> None:
        python_file = None
        if source_folder == "root":
            python_file = Path("main.py")
        else:
            python_file = Path(source_folder, "main.py")
        python_file.parent.mkdir(parents=True, exist_ok=True)
        self._logger.log("Added main.py")

        project_template = None
        try:
            template_path = os.path.join(
                self._templates_dir, f"{self._framework_id(framework)}.py"
            )
            with open(template_path, "r") as template_file:
                project_template = template_file.read()
            self._logger.log(f"Applied {self._framework_id(framework)} template")
        except FileNotFoundError:
            pass

        with open(python_file, "w") as f:
            if project_template is not None:
                f.write(project_template)

    def _pip_setup_project(self, dependencies: list[str]) -> None:
        self._logger.log("Creating virtual environment...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "venv",
                os.path.join(venv_dir),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            python_executable = os.path.abspath(
                os.path.join(venv_dir, "bin", "python3")
            )
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

    def _poetry_setup_project(self, dependencies: list[str]) -> None:
        subprocess.check_call(
            ["poetry", "init", "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._logger.log("Initialized poetry project")

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            custom_env = os.environ.copy()
            custom_env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
            custom_env["VIRTUAL_ENV"] = os.path.abspath(venv_dir)
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
            ["uv", "init", "--bare", "--no-workspace"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._logger.log("Initialized uv project")

        with open(".python-version", "w") as f:
            f.write(python_version)

        if len(dependencies) > 0:
            self._logger.log("Installing dependencies...")
            subprocess.check_call(
                [
                    "uv",
                    "add",
                    *dependencies,
                ],
            )

    def _django_setup_project(
        self, package_manager: Literal["pip", "poetry", "uv"], source_folder: str
    ) -> None:
        python_executable = os.path.abspath(os.path.join(venv_dir, "bin", "python3"))
        django_util = [python_executable, "-m", "django"]
        if package_manager == "uv":
            django_util = ["uv", "run", "django-admin"]
        self._logger.log("Initialized Django project")

        if source_folder != "root":
            os.chdir(source_folder)

        subprocess.check_call(
            [*django_util, "startproject", "mysite", "."],
        )


if __name__ == "__main__":
    fire.Fire(ProjectGenerator(logger=Logger()))
