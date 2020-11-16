import subprocess
import time
from datetime import datetime

import log


def decode_command_output_buffer(buffer):
    return buffer.decode("utf-8").strip()


def run_os_command(command_segments, cwd):
    res = subprocess.run(command_segments, capture_output=True, cwd=cwd)
    if res.returncode == 0:
        return True, decode_command_output_buffer(res.stdout)
    return False, decode_command_output_buffer(res.stderr)


def get_time_format_pattern():
    return "%Y/%m/%d %H:%M:%S"


def epoch_to_local_datetime(epoch_time):
    return time.strftime(get_time_format_pattern(), time.localtime(epoch_time))


def timestamp_utc0_formatted():
    return datetime.utcnow().strftime(get_time_format_pattern())


def log_rate_limit_status(tag, github_api):
    rl_status = github_api.request_rate_limit_status()
    log.info(tag,
             f"{rl_status['remaining']} calls remaining, resets at {epoch_to_local_datetime(rl_status['reset_at_utc'])}.")
