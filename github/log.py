import traceback
import sys
import os
from pathlib import Path

import util
from datetime import datetime


_log_file = None


def _define_log_file_path(specified_log_dir):
    """
    Establish the the correct path to the log file to be used. Does not create the file or check
    for its existence.
    :param specified_log_dir: string path to log file directory, or None
    :return: pathlib.Path to the log file
    """
    if specified_log_dir is None:
        specified_log_dir = os.getcwd()
    directory = util.ensure_directory(Path(specified_log_dir), Path(os.getcwd()))
    base_filename = datetime.now().strftime("%y%m%d-%H%M%S")
    file_path = directory.joinpath(f"{base_filename}.log")
    suffix_idx = 0
    while file_path.exists():
        suffix_idx += 1
        file_path = directory.joinpath(f"{base_filename}_{suffix_idx}.log")
    return file_path


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
    if _log_file is not None:
        _log_file.write(assembled_msg)
        _log_file.write("\n")
        _log_file.flush()


def _terminate(exit_code):
    """
    Terminate the application with the given exit code, performing all necessary pre-shutdown steps.
    :param exit_code: exit code to be used
    """
    global _log_file
    if _log_file is not None:
        _log_file.close()
    exit(exit_code)


def open_log_file(specified_log_dir):
    """
    Create and open a log file (all future logs will be written to this file). Do not create a file
    if one is already in use.
    :param specified_log_dir: string path to log file directory, or None
    """
    global _log_file
    if _log_file is not None:
        warning("LOGS", "Log file already open.")
        return
    file_path = _define_log_file_path(specified_log_dir)
    _log_file = open(file_path, "w", encoding="utf-8")
    info("LOGS", f"Logging to file '{file_path}'.")


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
