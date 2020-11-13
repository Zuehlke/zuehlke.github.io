import util
from datetime import datetime


def _log_message(level, tag, msg):
    print(f"[{timestamp()}] [{level}] [{tag}] {msg}")


def timestamp():
    return datetime.now().strftime(util.get_time_format_pattern())


def info(tag, msg):
    _log_message("INFO", tag, msg)


def warning(tag, msg):
    _log_message("WARN", tag, msg)


def error(tag, msg):
    _log_message("ERROR", tag, msg)


def abort_and_exit(tag, msg):
    _log_message("ABORT", tag, msg)
    exit(1)
