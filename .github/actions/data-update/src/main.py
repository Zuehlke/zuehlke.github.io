import os

import log
from pathlib import Path

import util
import jobs
from context import Context
from github_api import GitHubApi


def run_jobs(context, github_api):
    """
    Run predefined set of data update jobs.
    :param context: application context
    :param github_api: GitHub API wrapper
    """
    util.log_rate_limit_status("MAIN", github_api)
    jobs.JobCollectOrgRepos.initialize(context, github_api).run()
    # jobs.JobCollectOrgMembers.initialize(context, github_api).run()
    util.log_rate_limit_status("MAIN", github_api)


def main():
    # Absolute path of this script.
    script_path = Path(os.path.abspath(__file__))

    # Set up context and API wrappers.
    context = Context.create()
    github_api = GitHubApi(context)

    # Run jobs.
    run_jobs(context, github_api)

    # Terminate.
    log.terminate_successfully("MAIN")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        log.unhandled_exception_exit("MAIN", ex)
