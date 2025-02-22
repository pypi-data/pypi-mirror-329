from colorama import init, Fore

class Console:
    """
    A simple console utility for printing messages with color using colorama.
    """

    def __init__(self):
        init(autoreset=True)

    def log(self, message: str, end: str = "\n") -> None:
        print(message, end=end)

    def info(self, message: str, end: str = "\n") -> None:
        print(f"{Fore.BLUE}{message}", end=end)

    def warn(self, message: str, end: str = "\n") -> None:
        print(f"{Fore.YELLOW}{message}", end=end)

    def error(self, message: str, end: str = "\n") -> None:
        print(f"{Fore.RED}{message}", end=end)

    def success(self, message: str, end: str = "\n") -> None:
        print(f"{Fore.GREEN}{message}", end=end)

    def secondary(self, message: str, end: str = "\n") -> None:
        print(f"{Fore.LIGHTBLACK_EX}{message}", end=end)
