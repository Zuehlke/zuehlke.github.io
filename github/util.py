import subprocess


def fail_and_exit(msg):
    print(msg)
    exit(1)


def decode_command_output_buffer(buffer):
    return buffer.decode("utf-8").strip()


def run_os_command(command_segments, cwd):
    res = subprocess.run(command_segments, capture_output=True, cwd=cwd)
    if res.returncode == 0:
        return True, decode_command_output_buffer(res.stdout)
    return False, decode_command_output_buffer(res.stderr)
