from colorama import Fore, Style, init


class Logger:
    def __init__(self) -> None:
        init(autoreset=True)

    def log(self, message: str) -> None:
        print(Style.DIM + message)

    def success(self, message: str) -> None:
        print(Fore.GREEN + message)

    def error(self, message: str) -> None:
        print(Fore.RED + message)
