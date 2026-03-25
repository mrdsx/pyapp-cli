from typing import Any

from InquirerPy.separator import Separator


questions: list[dict[str, Any]] = [
    {
        "type": "input",
        "name": "project_path",
        "message": "Enter the project path",
    },
    {
        "type": "list",
        "name": "package_manager",
        "message": "Choose the package manager",
        "choices": ["pip", "poetry", "uv"],
    },
    {
        "type": "input",
        "name": "python_version",
        "message": "Enter Python version",
        "default": ">=3.12",
    },
    {
        "type": "list",
        "name": "source_folder",
        "message": "Choose the source code folder",
        "choices": [
            {"value": "root", "name": "root folder"},
            {"value": "src", "name": "./src"},
            {"value": "app", "name": "./app"},
        ],
    },
    {
        "type": "list",
        "name": "framework",
        "message": "Choose the framework",
        "choices": ["None", "FastAPI", "Flask", "Django"],
    },
    {
        "type": "checkbox",
        "name": "libraries",
        "message": "Choose the libraries",
        "choices": [
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
        ],
    },
]
