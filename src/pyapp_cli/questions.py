from typing import Any, Union

from InquirerPy import inquirer
from InquirerPy.separator import Separator

package_manager_choices: list[str] = ["pip", "poetry", "uv"]
source_folder_choices: list[dict[str, str]] = [
    {"value": "root", "name": "root folder"},
    {"value": "src", "name": "./src"},
    {"value": "app", "name": "./app"},
]
frameworks_choices: list[dict[str, str | None]] = [
    {"value": None, "name": "None"},
    {"value": "fastapi", "name": "FastAPI"},
    {"value": "flask", "name": "Flask"},
    {"value": "django", "name": "Django"},
]
libraries_choices: list[Union[str, Separator]] = [
    Separator(),
    "gunicorn",
    "uvicorn",
    Separator(),
    "sqlalchemy",
    "sqlmodel",
    "tortoise-orm",
    "firebase-admin",
    "supabase",
    Separator(),
    "pydantic",
    "pydantic-settings",
    "pytest",
    "pytest-asyncio",
    Separator(),
    "ruff",
    "black",
    "flake8",
    "pylint",
]


class Questions:
    def prompt(self) -> dict[str, Any]:
        project_path = inquirer.text(message="Enter the project path").execute()  # type: ignore
        package_manager = inquirer.select(  # type: ignore
            message="Choose the package manager",
            choices=package_manager_choices,
        ).execute()
        python_version = inquirer.text(  # type: ignore
            message="Enter Python version",
            default=">=3.12",
        ).execute()
        source_folder = inquirer.select(  # type: ignore
            message="Choose the source code folder",
            choices=source_folder_choices,
        ).execute()
        framework = inquirer.select(  # type: ignore
            message="Choose the framework",
            choices=frameworks_choices,
        ).execute()
        libraries = inquirer.checkbox(  # type: ignore
            message="Choose the libraries",
            choices=libraries_choices,
        ).execute()

        raw_answers: dict[str, Any] = {
            "project_path": project_path,
            "package_manager": package_manager,
            "python_version": python_version,
            "source_folder": source_folder,
            "framework": framework,
            "libraries": libraries,
        }

        return raw_answers
