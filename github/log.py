import traceback
import sys

import util
from datetime import datetime

_LEVEL_LENGTH = 7
_TAG_LENGTH = 4


def _log_message(level, tag, msg, stderr=False):
    for i in range(len(level), _LEVEL_LENGTH):
        level = level + " "
    for i in range(len(tag), _TAG_LENGTH):
        tag = tag + " "
    file = sys.stderr if stderr else sys.stdout
    print(f"[{timestamp()}] [{level}] [{tag}] {msg}", file=file)


def _terminate(exit_code):
    exit(exit_code)


def timestamp():
    return datetime.now().strftime(util.get_time_format_pattern())


def info(tag, msg):
    _log_message("INFO", tag, msg)


def warning(tag, msg):
    _log_message("WARNING", tag, msg)


def unhandled_exception_exit(tag, exception):
    _log_message("ERROR", tag, f"Uncaught {type(exception).__name__}: See traceback below.", stderr=True)
    _log_message("TRACE", tag, traceback.format_exc(), stderr=True)
    abort_and_exit(tag, "Exiting due to exception.")


def terminate_successfully(tag):
    _log_message("SUCCESS", tag, "Script execution terminated successfully.")
    _terminate(0)


def abort_and_exit(tag, msg):
    _log_message("ABORT", tag, msg, stderr=True)
    _terminate(1)
