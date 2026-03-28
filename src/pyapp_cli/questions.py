from typing import Any, Literal, Union

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from .schemas import Framework, PackageManager, SourceFolder

package_manager_choices: list[str] = [
    "pip",
    "poetry",
    "uv",
]
source_folder_choices: list[Choice] = [
    Choice(value="root", name="root folder"),
    Choice(value="src", name="./src"),
    Choice(value="app", name="./app"),
]
frameworks_choices: list[Choice] = [
    Choice(value=None, name="None"),
    Choice(value="fastapi", name="FastAPI"),
    Choice(value="flask", name="Flask"),
    Choice(value="django", name="Django"),
]
libraries_choices: list[Union[str, Separator]] = [
    "gunicorn",
    "uvicorn",
    Separator(),
    "aiosqlite",
    "psycopg",
    "asyncpg",
    "mysql-connector-python",
    "pymongo",
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
        libraries: str | None,
        no_libraries: Literal[True] | None,
    ) -> dict[str, Any]:
        if project_path is None:
            project_path = inquirer.text(  # pyright: ignore[reportPrivateImportUsage]
                message="Enter the project path"
            ).execute()

        if package_manager is None:
            package_manager = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                message="Choose the package manager",
                choices=package_manager_choices,
                show_cursor=False,
            ).execute()

        if python_version is None:
            python_version = inquirer.text(  # pyright: ignore[reportPrivateImportUsage]
                message="Enter Python version",
                default="3.12",
            ).execute()

        if source_folder is None:
            source_folder = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                message="Choose the source code folder",
                choices=source_folder_choices,
                show_cursor=False,
            ).execute()

        if framework is None:
            framework = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
                message="Choose the framework",
                choices=frameworks_choices,
                show_cursor=False,
            ).execute()

        _libraries = libraries
        if no_libraries is True and libraries is not None:
            raise TypeError(
                "Cannot set 'no_libraries' and 'libraries' at the same time"
            )
        elif no_libraries is True and libraries is None:
            _libraries = []
        elif no_libraries is None and libraries is None:
            _libraries = inquirer.checkbox(  # pyright: ignore[reportPrivateImportUsage]
                message="Choose the libraries",
                choices=libraries_choices,
                long_instruction="(You can add more by providing `--libraries` argument to `init` command)",
                height=10,
                cycle=False,
                show_cursor=False,
            ).execute()
        elif no_libraries is None and type(libraries) is str:
            _libraries = libraries.split(",")

        raw_answers: dict[str, Any] = {
            "project_path": project_path,
            "package_manager": package_manager,
            "python_version": python_version,
            "source_folder": source_folder,
            "framework": framework,
            "libraries": _libraries,
        }

        return raw_answers
