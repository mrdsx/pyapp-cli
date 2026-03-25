from typing import Literal

from pydantic import BaseModel

Framework = Literal["FastAPI", "Flask", "Django"]
PackageManager = Literal["pip", "poetry", "uv"]
SourceFolder = Literal["root", "src", "app"]


class Answers(BaseModel):
    project_path: str
    package_manager: PackageManager
    python_version: str
    source_folder: SourceFolder
    framework: Framework | None
    libraries: list[str]
