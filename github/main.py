import os

import log
from pathlib import Path

import util
import jobs
from context import Context
from git_wrapper import GitWrapper
from github_api import GitHubApi

# Path to data output directory, as segments relative to repository root
DATA_DIR = ["src", "data"]


def pull_source_repo(script_path):
    log.info("MAIN", "Pulling source repository.")
    context = Context.create(script_path)
    success, res = GitWrapper(context).pull_source_repo()
    if not success:
        log.abort_and_exit("MAIN", f"Failed to pull source repository: '{res}'")


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
    log.info("MAIN", f"Fetching workdir from targeted remote ({context.get_config('remote_name')}).")
    success = git.fetch_workdir()
    if not success:
        log.abort_and_exit("MAIN", "Failed to fetch workdir.")
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


def run_jobs(context, github_api):
    util.log_rate_limit_status("MAIN", github_api)
    jobs.JobCollectOrgRepos.initialize(context, github_api).run()
    jobs.JobCollectOrgMembers.initialize(context, github_api).run()
    util.log_rate_limit_status("MAIN", github_api)


def commit_and_push(context, git_wrapper):
    if not git_wrapper.workdir_has_uncommitted_changes():
        log.info("MAIN", "No changes to commit.")
        return
    commit_msg = f"[AUTO] Data updated at {util.timestamp_utc0_formatted()} UTC+0."
    log.info("MAIN", f"Committing changes with message '{commit_msg}'.")
    success, res = git_wrapper.commit_workdir_data_dir(commit_msg)
    if not success:
        log.abort_and_exit("MAIN", f"Failed to commit: '{res}'.")
    remote_name = context.get_config("remote_name")
    log.info("MAIN", f"Pushing branch '{context.get_config('target_branch')}' to remote '{remote_name}' at '{git_wrapper.get_workdir_remote_url(remote_name)}'.")
    success, res = git_wrapper.push_workdir_target_branch()
    if not success:
        log.abort_and_exit("MAIN", f"Failed to push: '{res}'.")
    log.info("MAIN", "Done.")


def main():
    # Absolute path of this script.
    script_path = Path(os.path.abspath(__file__))

    # Make sure source repository is up to date.
    pull_source_repo(script_path)

    # Set up context and API wrappers.
    context = Context.create(script_path)
    git_wrapper = GitWrapper(context)
    github_api = GitHubApi(context)

    # Set up secondary repo clone as workdir.
    setup_workdir_repo(context, git_wrapper)

    # Run jobs.
    run_jobs(context, github_api)

    # Commit and push.
    commit_and_push(context, git_wrapper)

    # Terminate.
    log.terminate_successfully("MAIN")


if __name__ == "__main__":
    main()
