import os

import github_api
import log
from pathlib import Path

import util
from context import Context
from git_wrapper import GitWrapper

# Path to data output directory, as segments relative to repository root
DATA_DIR = ["src", "data"]


def ensure_repo_clone(clone_path, context, git):
    source_remote_url = git.get_source_remote_url(context.get_config("remote_name"))

    if not clone_path.exists():
        # Workdir clone doesn't exist, creating.
        log.info("MAIN", f"Workdir doesn't exist - cloning '{source_remote_url}' into '{clone_path}'.")
        git.clone_repository(clone_path)
        return

    # Path already exists - make sure it is a directory.
    if not clone_path.is_dir():
        log.abort_and_exit("MAIN", f"Unable to establish workdir: '{clone_path}' exists but is not a directory.")

    # Path is a directory - make sure it is a git remote with the same remote as the source repo.
    remote_url = git.get_workdir_remote_url(context.get_config("remote_name"))
    if remote_url != source_remote_url:
        log.abort_and_exit("MAIN",
                           f"Workdir exists but has has incorrect remote: '{remote_url}' (expected '{source_remote_url}').")

    log.info("MAIN", f"Workdir already exists at '{clone_path}', no need to clone.")


def setup_workdir_repo(context, git):
    target_branch = context.get_config("target_branch")
    ensure_repo_clone(context.get_workdir_repo_root(), context, git)

    # Workdir clone now exists. Set up branch.
    success, res = git.ensure_workdir_branch(target_branch)
    if not success:
        log.abort_and_exit("MAIN", f"Failed to check out workdir branch '{target_branch}': {res}.")
    branch_tracked = git.is_target_branch_tracked()
    if branch_tracked:
        log.info("MAIN", f"Target branch '{target_branch}' is tracked - pulling.")
        success, res = git.pull_workdir_target_branch()
        if not success:
            log.abort_and_exit("MAIN", f"Failed to pull workdir repository: {res}.")
    else:
        log.info("MAIN", f"Target branch '{target_branch}' is not yet tracked - not pulling.")

    log.info("MAIN",
             f"Workdir repo '{context.get_workdir_repo_root()}' set up to {'tracked' if branch_tracked else 'untracked'} branch '{target_branch}'.")


def main():
    # update contribution repos
    # update people repos
    # git add ../src/data/contributions.json ../src/data/people.json
    # git commit -m "Automated update: contributions, people"
    # git push origin develop

    # Absolute path of this script.
    script_path = Path(os.path.abspath(__file__))

    # Set up context and Git wrapper.
    context = Context.initialize(script_path)
    git = GitWrapper(context)

    setup_workdir_repo(context, git)

    github = github_api.GitHubApi(context)
    rl_status = github.request_rate_limit_status()
    log.info("MAIN",
             f"{rl_status['remaining']} calls remaining, resets at {util.epoch_to_local_datetime(rl_status['reset_at_utc'])}.")
    repos = github.collect_org_repos()
    rl_status = github.request_rate_limit_status()
    log.info("MAIN",
             f"{rl_status['remaining']} calls remaining, resets at {util.epoch_to_local_datetime(rl_status['reset_at_utc'])}.")

    print(repos)


if __name__ == "__main__":
    main()
