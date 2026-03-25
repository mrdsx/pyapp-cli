from fire import Fire  # type: ignore

from .cli import CLI
from .logger import Logger
from .questions import Questions


def main() -> None:
    Fire(CLI(logger=Logger(), questions=Questions()))
