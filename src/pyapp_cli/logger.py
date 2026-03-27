from colorama import Fore, Style, init


class Logger:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        init(autoreset=True)

    def debug(self, message: str) -> None:
        if self.verbose:
            print(Style.DIM + f"[DEBUG] {message}")

    def log(self, message: str) -> None:
        print(message)

    def success(self, message: str) -> None:
        print(Fore.GREEN + message)

    def error(self, message: str) -> None:
        print(Fore.RED + message)
