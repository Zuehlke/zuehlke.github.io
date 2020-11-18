import util
import log


class GitWrapper:
    """Provides a wrapper for executing Git CLI commands."""

    def __init__(self, context):
        """
        Create a new GitWrapper.
        :param context: application context
        """
        self._context = context

    def _source_repo_command(self, command_segments):
        """
        Execute an OS command in the cwd context of the source repository root. In case of success,
        return the captured output to stdout. In case of failure (non-0 exit code), return the captured
        output to stderr.
        :param command_segments: segments of the OS command
        :return: success, output
        """
        return util.run_os_command(command_segments, self._context.get_source_repo_root())

    def _workdir_repo_command(self, command_segments):
        """
        Execute an OS command in the cwd context of the workdir repository root. In case of success,
        return the captured output to stdout. In case of failure (non-0 exit code), return the captured
        output to stderr.
        :param command_segments: segments of the OS command
        :return: success, output
        """
        return util.run_os_command(command_segments, self._context.get_workdir_repo_root())

    def fetch_workdir(self):
        """
        Fetch and prune the workdir repo.
        :return True of the command completed without errors, False else
        """
        success, _ = self._workdir_repo_command(["git", "fetch", "-p", self._context.get_config("remote_name")])
        return success

    def get_source_remote_url(self, remote_name):
        """
        Get the URL of the source repository's remote with the given name.
        :param remote_name: name of a remote of the source repository
        :return: remote URL
        """
        success, res = self._source_repo_command(["git", "remote", "get-url", remote_name])
        if not success:
            log.abort_and_exit("GITW", f"Unable to get URL for source remote '{remote_name}'.")
        return res

    def get_workdir_remote_url(self, remote_name):
        """
        Get the URL of the workdir repository's remote with the given name.
        :param remote_name: name of a remote of the workdir repository
        :return: remote URL
        """
        success, res = self._workdir_repo_command(["git", "remote", "get-url", remote_name])
        if not success:
            log.abort_and_exit("GITW", f"Unable to get URL for workdir remote '{remote_name}'.")
        return res

    def clone_repository(self, clone_path):
        """
        Create a clone of the source repository, using the URL of the remote specified in the config
        file. Clone to specified location.
        :param clone_path: root path of the new clone
        :return: success, output
        """
        remote_url = self.get_source_remote_url(self._context.get_config("remote_name"))
        return util.run_os_command(["git", "clone", remote_url, clone_path.name], clone_path.parent)

    def checkout_workdir_branch(self, branch_name):
        """
        Check out a given branch in the workdir repo.
        :param branch_name: name of the branch to check out
        :return: success, output
        """
        return self._workdir_repo_command(["git", "checkout", branch_name])

    def ensure_workdir_branch(self, branch_name):
        """
        Ensure that the given branch is checked out in the working directory - create it if needed.
        :param branch_name: name of the branch to check out and potentially create
        :return: success, output
        """
        success, res = self.checkout_workdir_branch(branch_name)
        if success:
            return success, res
        log.warning("GITW", f"Unable to check out workdir branch '{branch_name}', trying to create it.")
        return self._workdir_repo_command(["git", "checkout", "-b", branch_name])

    def is_target_branch_tracked(self):
        """
        Whether the target branch specified in the config file is tracked on the specified remote.
        :return: True if a remote branch with target branch's name is found on the specified remote, else False
        """
        success, res = self._workdir_repo_command(["git", "branch", "-r"])
        if not success:
            raise AssertionError("Should not reach here.")
        lines = [line.strip() for line in res.split("\n")]
        remote_branch_name = self._context.get_config("remote_name") + "/" + self._context.get_config("target_branch")
        return remote_branch_name in lines

    def pull_source_repo(self):
        """
        Pull the source repository.
        :return: success, output
        """
        return self._source_repo_command(["git", "pull"])

    def pull_workdir_target_branch(self):
        """
        Pull the specified target branch from the specified remote in the workdir repository.
        :return: success, output
        """
        remote_name = self._context.get_config("remote_name")
        target_branch = self._context.get_config("target_branch")
        return self._workdir_repo_command(["git", "pull", remote_name, target_branch])

    def commit_workdir_data_dir(self, commit_msg):
        """
        Stage all changes in the specified data directory in the workdir and create a commit. Returns False for
        success if there were no changes to commit.
        :param commit_msg: message to be provided during commit.
        :return: success, output
        """
        success, res = self._workdir_repo_command(["git", "add", self._context.get_workdir_data_dir_path()])
        if not success:
            log.abort_and_exit("GITW", f"Failed to add workdir data dir path: '{res}'.")
        return self._workdir_repo_command(["git", "commit", "-m", commit_msg])

    def workdir_has_uncommitted_changes(self):
        """
        Whether the workdir has uncommitted changes.
        :return: False if "git status" on the workdir repo outputs a line containing "nothing to commit", True else
        """
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
        """
        Push workdir's specified target branch to specified remote
        :return: success, output
        """
        remote_name = self._context.get_config("remote_name")
        target_branch = self._context.get_config("target_branch")
        return self._workdir_repo_command(["git", "push", remote_name, target_branch])


