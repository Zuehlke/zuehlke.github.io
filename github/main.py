import os
import json

import github_api
import git
import log
from pathlib import Path

import util
from context import Context

# Path to data output directory, as segments relative to repository root
DATA_DIR = ["src", "data"]


def read_config_file(script_path):
    file_path = script_path.parent.joinpath("config.json")
    try:
        with open(file_path) as infile:
            return json.load(infile)
    except FileNotFoundError:
        log.abort_and_exit("MAIN", f"Failed to read config file '{file_path}': not found.")


def ensure_repo_clone(clone_path, context):
    if not clone_path.exists():
        # Workdir clone doesn't exist, creating.
        log.info("MAIN", f"Workdir doesn't exist - cloning '{context.get_remote_url()}' into '{clone_path}'.")
        git.clone_repository(clone_path, context)
        return

    # Path already exists - make sure it is a directory.
    if not clone_path.is_dir():
        log.abort_and_exit("MAIN", f"Unable to establish workdir: '{clone_path}' exists but is not a directory.")

    # Path is a directory - make sure it is a git remote with the same remote as the source repo.
    success, remote = git.get_workdir_remote_url(context.get_config("remote_name"), context)
    if (not success) or (remote != context.get_remote_url()):
        log.abort_and_exit("MAIN",
                           f"Workdir exists but has has incorrect remote: '{remote}' (expected '{context.get_remote_url()}').")

    log.info("MAIN", f"Workdir already exists at '{clone_path}', no need to clone.")


def setup_workdir_repo(context):
    target_branch = context.get_config("target_branch")
    ensure_repo_clone(context.get_workdir_repo_root(), context)

    # Workdir clone now exists. Set up branch.
    success, res = git.ensure_workdir_branch(target_branch, context)
    if not success:
        log.abort_and_exit("MAIN", f"Failed to check out workdir branch '{target_branch}': {res}.")
    branch_tracked = git.is_branch_tracked(context)
    if branch_tracked:
        log.info("MAIN", f"Target branch '{target_branch}' is tracked - pulling.")
        success, res = git.pull_workdir_target_branch(context)
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

    context = Context()

    # Absolute path of this script.
    script_path = Path(os.path.abspath(__file__))

    context.set_config(read_config_file(script_path))
    context.set_source_repo_root(script_path.parent.parent)

    # Retrieve GitHub token from env var.
    token_env_var_name = context.get_config("github_api_token_envvar")
    github_token = os.getenv(token_env_var_name)
    if github_token is None:
        log.abort_and_exit("MAIN", f"Required env var '{token_env_var_name}' is not set.")
    context.set_github_token(github_token)

    # Directory containing the source repository.
    sources_root_parent = context.get_source_repo_root().parent

    # Root of the working directory (secondary clone on which to operate)
    context.set_workdir_repo_root(sources_root_parent.joinpath(context.get_config("workdir_root_dirname")))

    success, remote_url = git.get_source_remote_url(context.get_config("remote_name"), context)
    if not success:
        log.abort_and_exit("MAIN", f"Could not get remote URL of source repo: '{remote_url}'")
    context.set_remote_url(remote_url)

    setup_workdir_repo(context)

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
