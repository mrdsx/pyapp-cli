import fire

from .generator import ProjectGenerator
from .logger import Logger


def main() -> None:
    fire.Fire(ProjectGenerator(logger=Logger()))
