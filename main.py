import os
from pathlib import Path
import shutil
import subprocess
import sys

import fire
from InquirerPy import prompt

from questions import questions
from schemas import Answers

venv_dir = ".venv"


class ProjectGenerator:
    # frameworks that has to be installed as packages
    _framework_packages = set(["FastAPI", "Flask"])
    _templates_dir = os.path.abspath("templates")

    def init(self):
        raw_answers = prompt(questions)
        answers = Answers.model_validate(raw_answers)

        self._create_project_folder(answers.project_path)

        if answers.package_manager == "poetry":
            self._handle_poetry_setup()
        elif answers.package_manager == "uv":
            self._handle_uv_setup()

        if answers.framework == "None" or answers.framework in self._framework_packages:
            self._create_main_file(answers.source_folder, answers.framework)

        dependencies = answers.libraries
        if answers.framework in self._framework_packages:
            dependencies.append(self._framework_id(answers.framework))

        if answers.package_manager == "pip":
            self._pip_setup_project(dependencies)
        elif answers.package_manager == "poetry":
            self._poetry_setup_project(dependencies)
        elif answers.package_manager == "uv":
            self._uv_setup_project(dependencies, answers.python_version)

        print("Finished! Enjoy the project :)")

    def _framework_id(self, framework: str) -> str:
        return framework.lower()

    def _create_project_folder(self, project_path: str) -> None:
        print(f"Creating folder '{project_path}'.")
        Path(project_path).mkdir(exist_ok=True)
        os.chdir(project_path)

    def _handle_poetry_setup(self) -> None:
        poetry_exists = shutil.which("poetry") is not None
        if poetry_exists:
            print("Poetry is already installed.")
        else:
            print("Installing pipx...")
            subprocess.check_call(
                [
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "--user",
                    "pipx",
                    "--break-system-packages",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("Installing poetry...")
            subprocess.check_call(
                ["pipx", "install", "poetry", "--force"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("Poetry is installed.")

    def _handle_uv_setup(self) -> None:
        uv_exists = shutil.which("uv") is not None
        if uv_exists:
            print("uv is already installed.")
        else:
            print("Installing pipx...")
            subprocess.check_call(
                [
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "--user",
                    "pipx",
                    "--break-system-packages",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("Installing uv...")
            subprocess.check_call(
                ["pipx", "install", "uv", "--force"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("uv is installed.")

    def _create_main_file(self, source_folder: str, framework: str) -> None:
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
        print("Creating virtual environment...")
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
            print("Installing dependencies...")
            python_executable = os.path.abspath(
                os.path.join(venv_dir, "bin", "python3")
            )
            subprocess.check_call(
                [python_executable, "-m", "pip", "install", *dependencies],
            )

    def _poetry_setup_project(self, dependencies: list[str]) -> None:
        print("Initializing project...")
        subprocess.check_call(
            ["poetry", "init", "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if len(dependencies) > 0:
            print("Installing dependencies...")
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
        print("Initializing project...")
        subprocess.check_call(["uv", "init", "--bare", "--no-workspace"])

        with open(".python-version", "w") as f:
            f.write(python_version)

        if len(dependencies) > 0:
            print("Installing dependencies...")
            subprocess.check_call(
                [
                    "uv",
                    "add",
                    *dependencies,
                ],
            )


if __name__ == "__main__":
    fire.Fire(ProjectGenerator)
