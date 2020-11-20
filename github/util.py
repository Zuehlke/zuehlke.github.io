import subprocess
import time
from datetime import datetime

import log


def decode_command_output_buffer(buffer):
    return buffer.decode("utf-8").strip()


def run_os_command(command_segments, cwd):
    """
    Execute an OS command in a given cwd context. In case of success, return the captured output
    to stdout. In case of failure (non-0 exit code), return the captured output to stderr.
    :param command_segments: segments of the OS command
    :param cwd: current working directory path to be used as the execution context
    :return: success, output
    """
    res = subprocess.run(command_segments, capture_output=True, cwd=cwd)
    if res.returncode == 0:
        return True, decode_command_output_buffer(res.stdout)
    return False, decode_command_output_buffer(res.stderr)


def get_time_format_pattern():
    """
    Return default datetime format string.
    :return: default datetime format string
    """
    return "%Y/%m/%d %H:%M:%S"


def epoch_to_local_datetime(epoch_time):
    """
    Convert an UTC epoch value to a formatted date and time string in local time.
    :param epoch_time: epoch seconds value
    :return: formatted local date and time string
    """
    return time.strftime(get_time_format_pattern(), time.localtime(epoch_time))


def timestamp_utc0_formatted():
    """
    Get current UTC+0 date and time as a formatted string.
    :return: current UTC+0 date and time as formatted string
    """
    return datetime.utcnow().strftime(get_time_format_pattern())


def log_rate_limit_status(tag, github_api):
    """
    Log the current rate limit status.
    :param tag: log location identifier
    :param github_api: GitHub API wrapper
    """
    rl_status = github_api.request_rate_limit_status()
    log.info(tag,
             f"{rl_status['remaining']} calls remaining, resets at {epoch_to_local_datetime(rl_status['reset_at_utc'])}.")


def ensure_directory(dirname, relative_to, create_parents=True):
    """
    Ensure that a given directory exists, creating it (and optionally its parents) if required.
    :param dirname: string path (absolute or relative) to the directory to be ensured
    :param relative_to: root posix.Path to be used in case dirname is a relative path, or None
    :param create_parents: whether to create the directory's parents if required (True)
    :return: posix.Path the specified directory, now guaranteed to exist unless removed
    """
    path = dirname
    if not dirname.is_absolute():
        path = relative_to.joinpath(dirname)
    if path.exists():
        assert not path.is_file(), "Expected directory, found existing file."
        return path
    path.mkdir(parents=create_parents)
    assert path.exists(), "Expected directory to exist after creation."
    return path
