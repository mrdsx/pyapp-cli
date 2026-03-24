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
    framework_packages = set(["FastAPI", "Flask"])

    def init(self):
        raw_answers = prompt(questions)
        answers = Answers.model_validate(raw_answers)

        # generate project folder
        print(f"Creating folder '{answers.project_path}'.")
        Path(answers.project_path).mkdir(exist_ok=True)
        os.chdir(answers.project_path)

        # install package manager if not installed
        if answers.package_manager == "poetry":
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
        elif answers.package_manager == "uv":
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

        # create main.py file
        if answers.framework == "None" or answers.framework in self.framework_packages:
            python_file = None
            if answers.source_folder == "root":
                python_file = Path("main.py")
            else:
                python_file = Path(answers.source_folder, "main.py")
            python_file.parent.mkdir(parents=True, exist_ok=True)

            project_template = None
            try:
                template_file = open(
                    os.path.join("../templates", f"{answers.framework.lower()}.py"), "r"
                )
                project_template = template_file.read()
            except FileNotFoundError:
                pass

            with open(python_file, "w") as f:
                if project_template is not None:
                    f.write(project_template)

        # initialize project and install dependencies
        dependencies = answers.libraries
        if answers.framework in self.framework_packages:
            dependencies.append(self.__framework_id(answers.framework))

        if answers.package_manager == "pip":
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
        elif answers.package_manager == "poetry":
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
        elif answers.package_manager == "uv":
            print("Initializing project...")
            subprocess.check_call(["uv", "init", "--bare", "--no-workspace"])

            with open(".python-version", "w") as f:
                f.write(answers.python_version)

            if len(dependencies) > 0:
                print("Installing dependencies...")
                subprocess.check_call(
                    [
                        "uv",
                        "add",
                        *dependencies,
                    ],
                )

        print("Finished! Enjoy the project :)")

    def __framework_id(self, framework: str) -> str:
        return framework.lower()


if __name__ == "__main__":
    fire.Fire(ProjectGenerator)
