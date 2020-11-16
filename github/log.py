import util
from datetime import datetime

_LEVEL_LENGTH = 7
_TAG_LENGTH = 4


def _log_message(level, tag, msg):
    for i in range(len(level), _LEVEL_LENGTH):
        level = level + " "
    for i in range(len(tag), _TAG_LENGTH):
        tag = tag + " "
    print(f"[{timestamp()}] [{level}] [{tag}] {msg}")


def timestamp():
    return datetime.now().strftime(util.get_time_format_pattern())


def info(tag, msg):
    _log_message("INFO", tag, msg)


def warning(tag, msg):
    _log_message("WARNING", tag, msg)


def terminate_successfully(tag):
    _log_message("SUCCESS", tag, "Script execution terminated successfully.")
    exit(0)


def abort_and_exit(tag, msg):
    _log_message("ABORT", tag, msg)
    exit(1)
