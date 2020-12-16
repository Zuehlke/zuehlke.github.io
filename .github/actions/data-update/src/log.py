import traceback
import sys

import util
from datetime import datetime


def _log_message(level, tag, msg, stderr=False):
    """
    Log to console and to file if one is being used.
    :param level: log level (4-character string)
    :param tag: log location identifier (4-character string)
    :param msg: message to be logged
    :param stderr: whether to log to stderr instead of stdout (False)
    """
    assembled_msg = f"[{timestamp()}] [{level}] [{tag}] {msg}"
    file = sys.stderr if stderr else sys.stdout
    print(assembled_msg, file=file)


def _terminate(exit_code):
    """
    Terminate the application with the given exit code, performing all necessary pre-shutdown steps.
    :param exit_code: exit code to be used
    """
    exit(exit_code)


def timestamp():
    """
    Get formatted local date and time.
    :return: formatted local date and time
    """
    return datetime.now().strftime(util.get_time_format_pattern())


def info(tag, msg):
    """
    Log an info-level message to stdout and to log file if applicable.
    :param tag: log location identifier (4-character string)
    :param msg: message to be logged
    """
    _log_message("INFO", tag, msg)


def warning(tag, msg):
    """
    Log a warning-level message to stdout and to log file if applicable.
    :param tag: log location identifier (4-character string)
    :param msg: message to be logged
    """
    _log_message("WARN", tag, msg)


def error(tag, msg):
    """
    Log an error-level message to stderr and to log file if applicable.
    :param tag: log location identifier (4-character string)
    :param msg: message to be logged
    """
    _log_message("ERR!", tag, msg, stderr=True)


def unhandled_exception_exit(tag, exception):
    """
    Log an exception stack trace to stderr and to log file if applicable.
    :param tag: log location identifier (4-character string)
    :param exception: exception to be logged
    """
    error(tag, f"Uncaught {type(exception).__name__}: See traceback below.")
    _log_message("TBCK", tag, traceback.format_exc(), stderr=True)
    abort_and_exit(tag, "Exiting due to exception.")


def terminate_successfully(tag):
    """
    Terminate the application with success exit code.
    :param tag: log location identifier (4-character string)
    """
    _log_message("DONE", tag, "Script execution terminated successfully.")
    _terminate(0)


def abort_and_exit(tag, msg):
    """
    Log an error-level message and terminate the application with non-0 exit code.
    :param tag: log location identifier (4-character string)
    :param msg: message to be logged
    """
    error(tag, msg)
    _log_message("HALT", tag, "Execution terminated with errors.", stderr=True)
    _terminate(1)
