import os
import json
import util
import git
from pathlib import Path
from context import Context

# Branch on which to operate
TARGET_BRANCH = "topic/github_api_access"

# Path to data output directory, as segments relative to repository root
DATA_DIR = ["src", "data"]


def read_config(script_path):
    with open(script_path.parent.joinpath("config.json"), "r") as infile:
        return json.load(infile)


def ensure_repo_clone(clone_path, context):
    if not clone_path.exists():
        # Workdir clone doesn't exist, creating.
        print(f"Workdir doesn't exist - cloning {context.get_remote_url()} into {clone_path}.")
        git.clone_repository(clone_path, context)
        return

    # Path already exists - make sure it is a directory.
    if not clone_path.is_dir():
        util.fail_and_exit(f"Unable to establish workdir: {clone_path} exists but is not a directory.")

    # Path is a directory - make sure it is a git remote with the same remote as the source repo.
    success, remote = git.get_workdir_remote_url(context.get_config()["remote_name"], context)
    if (not success) or (remote != context.get_remote_url()):
        util.fail_and_exit(
            f"Workdir exists but has has incorrect remote: {remote} (expected {context.get_remote_url()}).")

    print(f"Workdir already exists at {clone_path}, no need to clone.")


def setup_workdir_repo(context):
    target_branch = context.get_config()["target_branch"]
    ensure_repo_clone(context.get_workdir_repo_root(), context)

    # Workdir clone now exists. Set up branch.
    success, res = git.ensure_workdir_branch(target_branch, context)
    if not success:
        util.fail_and_exit(f"Failed to check out workdir branch {target_branch}: {res}.")
    branch_tracked = git.is_branch_tracked(context)
    if branch_tracked:
        print(f"Target branch {target_branch} is tracked - pulling.")
        success, res = git.pull_workdir_target_branch(context)
        if not success:
            util.fail_and_exit(f"Failed to pull workdir repository: {res}.")
    else:
        print(f"Target branch {target_branch} is not yet tracked - not pulling.")

    print(f"Workdir repo {context.get_workdir_repo_root()} set up to {'tracked' if branch_tracked else 'untracked'} branch {target_branch}.")


def main():
    # update contribution repos
    # update people repos
    # git add ../src/data/contributions.json ../src/data/people.json
    # git commit -m "Automated update: contributions, people"
    # git push origin develop

    context = Context()

    # Absolute path of this script.
    script_path = Path(os.path.abspath(__file__))

    context.set_config(read_config(script_path))
    context.set_source_repo_root(script_path.parent.parent)

    # Directory containing the source repository.
    sources_root_parent = context.get_source_repo_root().parent

    # Root of the working directory (secondary clone on which to operate)
    context.set_workdir_repo_root(sources_root_parent.joinpath(context.get_config()["workdir_root_dirname"]))

    success, remote_url = git.get_source_remote_url(context.get_config()["remote_name"], context)
    if not success:
        util.fail_and_exit(f"Could not get remote URL of source repo: {remote_url}")
    context.set_remote_url(remote_url)

    setup_workdir_repo(context)


if __name__ == "__main__":
    main()
