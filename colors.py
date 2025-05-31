
from colorama import Fore, Style, init

# Khởi tạo colorama
init(autoreset=True)

class Colors:
    HEADER = Fore.MAGENTA + Style.BRIGHT
    PROMPT = Fore.YELLOW + Style.BRIGHT
    RESPONSE = Fore.GREEN
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.CYAN
    FRAME = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
    DIVIDER = Fore.LIGHTBLUE_EX + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    RESET = Style.RESET_ALL
