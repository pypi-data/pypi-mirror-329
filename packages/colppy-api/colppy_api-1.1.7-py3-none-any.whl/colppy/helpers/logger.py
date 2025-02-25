from colorama import Fore, Style, init


init(autoreset=True)

LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 10,
    'WARNING': 20,
    'ERROR': 30,
    'CRITICAL': 40
}

LOG_COLORS = {
    'DEBUG': Fore.BLUE,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.MAGENTA
}


class Logger:
    def __init__(self, name):
        self._name = name
        self._log_level = LOG_LEVELS.get("DEBUG")

    def _log(self, level, msg):
        if level >= self._log_level:
            color = LOG_COLORS.get(list(LOG_LEVELS.keys())[list(LOG_LEVELS.values()).index(level)], "")
            print(f"{self._name} - {color}{msg}{Style.RESET_ALL}")

    def debug(self, message):
        self._log(LOG_LEVELS["DEBUG"], f"DEBUG: {message}")

    def info(self, message):
        self._log(LOG_LEVELS["INFO"], f"INFO: {message}")

    def warning(self, message):
        self._log(LOG_LEVELS["WARNING"], f"WARNING: {message}")

    def error(self, message):
        self._log(LOG_LEVELS["ERROR"], f"ERROR: {message}")

    def critical(self, message):
        self._log(LOG_LEVELS["CRITICAL"], f"CRITICAL: {message}")


logger = Logger("Colppy")
