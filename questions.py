questions = [
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
        "default": "3.12",
    },
    {
        "type": "list",
        "name": "source_folder",
        "message": "Choose the source code folder",
        "choices": ["./src", "./app", "root (current directory)"],
    },
    {
        "type": "list",
        "name": "framework",
        "message": "Choose the framework",
        "choices": ["None", "FastAPI"],
    },
    {
        "type": "checkbox",
        "name": "libraries",
        "message": "Choose the libraries",
        "choices": [
            "uvicorn",
            "sqlalchemy",
            "firebase-admin",
            "pydantic",
            "pydantic-settings",
            "pytest",
        ],
    },
]
