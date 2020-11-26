import time

import log


def decode_command_output_buffer(buffer):
    return buffer.decode("utf-8").strip()


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


def log_rate_limit_status(tag, github_api):
    """
    Log the current rate limit status.
    :param tag: log location identifier
    :param github_api: GitHub API wrapper
    """
    rl_status = github_api.request_rate_limit_status()
    log.info(tag,
             f"{rl_status['remaining']} calls remaining, resets at {epoch_to_local_datetime(rl_status['reset_at_utc'])}.")
