import jobs
import log
import util
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
    jobs.JobCollectExternalRepos.initialize(context, github_api).run()
    jobs.JobCollectOrgMembers.initialize(context, github_api).run()
    jobs.JobWriteLastUpdate.initialize(context).run()
    util.log_rate_limit_status("MAIN", github_api)


def main():
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
