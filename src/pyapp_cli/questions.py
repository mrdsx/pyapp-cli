from typing import Any, Union

from InquirerPy import inquirer
from InquirerPy.separator import Separator

from .schemas import Framework, PackageManager, SourceFolder

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
    def prompt(
        self,
        project_path: str | None,
        package_manager: PackageManager | None,
        python_version: str | None,
        source_folder: SourceFolder | None,
        framework: Framework | None,
        libraries: list[str] | None,
    ) -> dict[str, Any]:
        if project_path is None:
            project_path = inquirer.text(  # pyright: ignore[reportPrivateImportUsage]
                message="Enter the project path"
            ).execute()

        if package_manager is None:
            package_manager = (
                inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                    message="Choose the package manager",
                    choices=package_manager_choices,
                ).execute()
            )

        if python_version is None:
            python_version = inquirer.text(  # pyright: ignore[reportPrivateImportUsage]
                message="Enter Python version",
                default="3.12",
            ).execute()

        if source_folder is None:
            source_folder = (
                inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                    message="Choose the source code folder",
                    choices=source_folder_choices,
                ).execute()
            )

        if framework is None:
            framework = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                message="Choose the framework",
                choices=frameworks_choices,
            ).execute()

        if libraries is None:
            libraries = inquirer.checkbox(  # pyright: ignore[reportPrivateImportUsage]
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
