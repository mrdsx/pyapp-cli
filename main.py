import os
from pathlib import Path
import shutil
import subprocess

import fire
from InquirerPy import prompt

from questions import questions
from schemas import Answers


class ProjectGenerator:
    def init(self):
        raw_answers = prompt(questions)
        answers = Answers.model_validate(raw_answers)

        # generate project folder
        print(f"Creating folder '{answers.project_path}'.")
        Path(answers.project_path).mkdir(exist_ok=True)

        # install package manager if not installed
        if answers.package_manager == "poetry":
            poetry_exists = shutil.which("poetry") is not None
            if poetry_exists:
                print("Poetry is already installed.")
            else:
                print("Installing pipx...")
                subprocess.run(
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
                subprocess.run(
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
                subprocess.run(
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
                subprocess.run(
                    ["pipx", "install", "uv", "--force"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print("uv is installed.")

        # create main.py file
        python_file = None
        if answers.source_folder == "root":
            python_file = Path(answers.project_path, "main.py")
        else:
            python_file = Path(answers.project_path, answers.source_folder, "main.py")
        python_file.parent.mkdir(parents=True, exist_ok=True)
        with open(python_file, "w"):
            pass


if __name__ == "__main__":
    fire.Fire(ProjectGenerator)
