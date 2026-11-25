import gzip
import sys
import colorama
import asyncio

from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from colorama import Fore


colorama.init(autoreset=True)

@dataclass
class ConsoleConfig:
    use_log_file: bool = True
    log_folder: str = "logs"
    gzip_old_logs: bool = True
    old_logs_count: int = 100
    latest_file_name: str = "latest.log"

_run_folder: Path | None = None

def _GetTimeStamp(format: str) -> str:
    return str(datetime.now().strftime(format))

def _GetCaller() -> str:
    try:
        script_name = str(sys._getframe(2).f_globals.get('__name__', 'Unknown'))
        
        if str(script_name) == "__main__":
            return "Main"
        else:
            return str(script_name)
    except Exception:
        return "Unknown"

def _FallbackLogger(Output: str | None):
    print(f"[{Fore.RED}FALLBACK CONSOLE{Fore.RESET}]: {str(Output)}")

def _log(ForeColor = Fore.CYAN, LogType: str = "I", Output: str | None = None, Caller: str = ""):
    time = str(str(_GetTimeStamp("%Y-%m-%d %H:%M:%S.%f"))[:-3])

    log_msg = f"{str(time)} {str(Caller)} {str(LogType)} {"" if Output is None else str(Output)}"
    print_msg = f"{str(time)} {Fore.CYAN}{str(Caller)}{Fore.RESET} {ForeColor}{str(LogType)}{Fore.RESET} {"" if Output is None else str(Output)}"

    print(str(print_msg), flush = True)


async def init(config: ConsoleConfig | None = None):
    global _run_folder

    _run_folder = Path.cwd()


def log(text: str | None = None):
    caller = str(_GetCaller())

    _log(
        ForeColor = Fore.GREEN,
        LogType = "L",
        Output = text,
        Caller = caller
    )

def info(text: str | None = None):
    caller = str(_GetCaller())

    _log(
        ForeColor = Fore.CYAN,
        LogType = "I",
        Output = text,
        Caller = caller
    )

def warn(text: str | None = None):
    caller = str(_GetCaller())

    _log(
        ForeColor = Fore.YELLOW,
        LogType = "W",
        Output = text,
        Caller = caller
    )

def error(text: str | None = None):
    caller = str(_GetCaller())

    _log(
        ForeColor = Fore.RED,
        LogType = "E",
        Output = text,
        Caller = caller
    )

def debug(text: str | None = None):
    caller = str(_GetCaller())

    _log(
        ForeColor = Fore.MAGENTA,
        LogType = "D",
        Output = text,
        Caller = caller
    )