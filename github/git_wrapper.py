import util
import log


class GitWrapper:

    def __init__(self, context):
        self._context = context

    def _source_repo_command(self, command_segments):
        return util.run_os_command(command_segments, self._context.get_source_repo_root())

    def _workdir_repo_command(self, command_segments):
        return util.run_os_command(command_segments, self._context.get_workdir_repo_root())

    def fetch_workdir(self):
        success, _ = self._workdir_repo_command(["git", "fetch", self._context.get_config("remote_name")])
        return success

    def get_source_remote_url(self, remote_name):
        success, res = self._source_repo_command(["git", "remote", "get-url", remote_name])
        if not success:
            log.abort_and_exit("GITW", f"Unable to get URL for source remote '{remote_name}'.")
        return res

    def get_workdir_remote_url(self, remote_name):
        success, res = self._workdir_repo_command(["git", "remote", "get-url", remote_name])
        if not success:
            log.abort_and_exit("GITW", f"Unable to get URL for workdir remote '{remote_name}'.")
        return res

    def clone_repository(self, clone_path):
        remote_url = self.get_source_remote_url(self._context.get_config("remote_name"))
        return util.run_os_command(["git", "clone", remote_url, clone_path.name], clone_path.parent)

    def checkout_workdir_branch(self, branch_name):
        return self._workdir_repo_command(["git", "checkout", branch_name])

    def ensure_workdir_branch(self, branch_name):
        success, res = self.checkout_workdir_branch(branch_name)
        if success:
            return success, res
        log.warning("GITW", f"Unable to check out workdir branch '{branch_name}', trying to create it.")
        return self._workdir_repo_command(["git", "checkout", "-b", branch_name])

    def is_target_branch_tracked(self):
        success, res = self._workdir_repo_command(["git", "branch", "-r"])
        if not success:
            # TODO: Catch and report all exceptions in main, or find better solution to this.
            raise AssertionError("Should not reach here.")
        lines = [line.strip() for line in res.split("\n")]
        remote_branch_name = self._context.get_config("remote_name") + "/" + self._context.get_config("target_branch")
        return remote_branch_name in lines

    def pull_workdir_target_branch(self):
        remote_name = self._context.get_config("remote_name")
        target_branch = self._context.get_config("target_branch")
        return self._workdir_repo_command(["git", "pull", remote_name, target_branch])

    def commit_workdir_data_dir(self, commit_msg):
        success, res = self._workdir_repo_command(["git", "add", self._context.get_workdir_data_dir_path()])
        if not success:
            log.abort_and_exit("GITW", f"Failed to add workdir data dir path: '{res}'.")
        return self._workdir_repo_command(["git", "commit", "-m", commit_msg])

    def workdir_has_uncommitted_changes(self):
        success, res = self._workdir_repo_command(["git", "status"])
        if not success:
            log.abort_and_exit("GITW", f"Failed to query git status: '{res}'.")
        for line in res.splitlines():
            if "nothing to commit" in line.lower():
                # Found line including "nothing to commit" - no uncommitted changes.
                return False
        # Found no line saying "nothing to commit" - assuming uncommitted changes.
        return True

    def push_workdir_target_branch(self):
        remote_name = self._context.get_config("remote_name")
        target_branch = self._context.get_config("target_branch")
        return self._workdir_repo_command(["git", "push", remote_name, target_branch])


