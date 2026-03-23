from typing import Literal

from pydantic import BaseModel


class Answers(BaseModel):
    project_path: str
    package_manager: Literal["pip", "poetry", "uv"]
    python_version: str
    source_folder: Literal["root", "src", "app"]
    framework: Literal["None", "FastAPI"]
    libraries: list[str]
