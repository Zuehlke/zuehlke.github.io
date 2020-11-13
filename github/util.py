import subprocess
import time


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
