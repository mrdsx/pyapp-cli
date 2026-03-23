import os
import shutil
import subprocess
import sys

import fire
from InquirerPy import prompt

from questions import questions
from schemas import Answers


class ProjectGenerator:
    def init(self):
        raw_answers = prompt(questions)
        answers = Answers.model_validate(raw_answers)

        # generate project folder
        try:
            print(f"Creating folder '{answers.project_path}'.")
            os.mkdir(answers.project_path)
        except FileExistsError:
            pass

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


if __name__ == "__main__":
    fire.Fire(ProjectGenerator)
