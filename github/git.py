import util


def _source_repo_command(command_segments, context):
    return util.run_os_command(command_segments, context.get_source_repo_root())


def _workdir_repo_command(command_segments, context):
    return util.run_os_command(command_segments, context.get_workdir_repo_root())


def get_source_remote_url(remote_name, context):
    return _source_repo_command(["git", "remote", "get-url", remote_name], context)


def get_workdir_remote_url(remote_name, context):
    return _workdir_repo_command(["git", "remote", "get-url", remote_name], context)


def clone_repository(clone_path, context):
    return util.run_os_command(["git", "clone", context.get_remote_url(), clone_path.name], clone_path.parent)


def checkout_workdir_branch(branch_name, context):
    return _workdir_repo_command(["git", "checkout", branch_name], context)


def ensure_workdir_branch(branch_name, context):
    success, res = checkout_workdir_branch(branch_name, context)
    if success:
        return success, res
    print(f"Unable to check out workdir branch {branch_name}, trying to create it.")
    return _workdir_repo_command(["git", "checkout", "-b", branch_name], context)


def is_branch_tracked(context):
    success, res = _workdir_repo_command(["git", "branch", "-r"], context)
    if not success:
        # TODO: Catch and report all exceptions in main, or find better solution to this.
        raise AssertionError("Should not reach here.")
    lines = [line.strip() for line in res.split("\n")]
    remote_branch_name = context.get_config()["remote_name"] + "/" + context.get_config()["target_branch"]
    return remote_branch_name in lines


def pull_workdir_target_branch(context):
    config = context.get_config()
    return _workdir_repo_command(["git", "pull", config["remote_name"], config["target_branch"]], context)


def push_workdir_target_branch(context):
    config = context.get_config()
    return _workdir_repo_command(["git", "push", config["remote_name"], config["target_branch"]], context)
