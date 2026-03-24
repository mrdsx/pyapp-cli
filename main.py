import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Literal

from colorama import Fore, Style, init
import fire
from InquirerPy import prompt

from questions import questions
from schemas import Answers

venv_dir = ".venv"


class ProjectGenerator:
    # frameworks without built-in CLI for scaffolding the project
    _framework_packages = set(["FastAPI", "Flask"])
    _templates_dir = os.path.abspath("templates")

    def init(self):
        init(autoreset=True)
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

        print(Fore.GREEN + "Finished! Enjoy the project :)")

    def _framework_id(self, framework: str) -> str:
        return framework.lower()

    def _missing_dependency_message(self, dependency: str) -> str:
        return Fore.RED + (
            f"Can't detect installed {dependency}.\n"
            f"Ensure {dependency} is installed and then run the script again."
        )

    def _create_project_folder(self, project_path: str, source_folder: str) -> None:
        print(Style.DIM + f"Creating folder '{project_path}'...")
        Path(project_path).mkdir(exist_ok=True)
        if source_folder != "root":
            Path(project_path, source_folder).mkdir(exist_ok=True)
        os.chdir(project_path)

    def _ensure_pip_installation(self) -> None:
        pip_exists = shutil.which("pip") is not None
        if pip_exists:
            print(Fore.GREEN + "pip is already installed.")
        else:
            print(self._missing_dependency_message("pip"))
            exit(127)

    def _ensure_poetry_installation(self) -> None:
        poetry_exists = shutil.which("poetry") is not None
        if poetry_exists:
            print(Fore.GREEN + "Poetry is already installed.")
        else:
            print(self._missing_dependency_message("Poetry"))
            exit(127)

    def _ensure_uv_installation(self) -> None:
        uv_exists = shutil.which("uv") is not None
        if uv_exists:
            print(Fore.GREEN + "uv is already installed.")
        else:
            print(self._missing_dependency_message("uv"))
            exit(127)

    def _create_main_file(self, source_folder: str, framework: str) -> None:
        print(Style.DIM + "Creating main.py file...")
        python_file = None
        if source_folder == "root":
            python_file = Path("main.py")
        else:
            python_file = Path(source_folder, "main.py")
        python_file.parent.mkdir(parents=True, exist_ok=True)

        project_template = None
        try:
            template_path = os.path.join(
                self._templates_dir, f"{self._framework_id(framework)}.py"
            )
            with open(template_path, "r") as template_file:
                project_template = template_file.read()
        except FileNotFoundError:
            pass

        with open(python_file, "w") as f:
            if project_template is not None:
                f.write(project_template)

    def _pip_setup_project(self, dependencies: list[str]) -> None:
        print(Style.DIM + "Creating virtual environment...")
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
            print(Style.DIM + "Installing dependencies...")
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

    def _poetry_setup_project(self, dependencies: list[str]) -> None:
        print(Style.DIM + "Initializing project...")
        subprocess.check_call(
            ["poetry", "init", "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if len(dependencies) > 0:
            print(Style.DIM + "Installing dependencies...")
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
        print(Style.DIM + "Initializing project...")
        subprocess.check_call(
            ["uv", "init", "--bare", "--no-workspace"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with open(".python-version", "w") as f:
            f.write(python_version)

        if len(dependencies) > 0:
            print(Style.DIM + "Installing dependencies...")
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
        print(Style.DIM + "Initializing Django project...")

        python_executable = os.path.abspath(os.path.join(venv_dir, "bin", "python3"))
        django_util = [python_executable, "-m", "django"]
        if package_manager == "uv":
            django_util = ["uv", "run", "django-admin"]

        if source_folder != "root":
            os.chdir(source_folder)

        subprocess.check_call(
            [*django_util, "startproject", "mysite", "."],
        )


if __name__ == "__main__":
    fire.Fire(ProjectGenerator)
