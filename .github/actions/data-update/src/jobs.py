import json

import consts
import log


class Job:
    """
    Represents an automation job which may involve data collection, data provisioning and file writes. A
    job does not include any Git operations such as committing or pushing.
    """

    def __init__(self, job_name, context, github_api):
        """
        Private constructor.
        :param job_name: display name of the job
        :param context: application context
        :param github_api: GitHub API wrapper
        """
        self._job_name = job_name
        self._context = context
        self._github_api = github_api

    def _write_to_json_file(self, filename, data):
        """
        Write data into a file in the predefined output directory.
        :param filename: name of the file (no path), should end in .json
        :param data: JSON-serializable object
        """
        out_dir_path = self._context.get_data_dir_path()
        filepath = out_dir_path.joinpath(filename)
        log.info(filepath)
        try:
            with open(filepath, "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=2)
        except FileNotFoundError:
            log.abort_and_exit("JOBS", f"Output directory path '{out_dir_path}' not found.")

    def run(self):
        """
        Execute this job.
        """
        log.info("JOBS", f"Starting job '{self._job_name}'.")
        self._execute_task()
        log.info("JOBS", f"Completed job '{self._job_name}'.")

    def _execute_task(self):
        """
        Abstract method, define tasks of this job.
        """
        raise NotImplementedError


class JobCollectOrgRepos(Job):

    def __init__(self, context, github_api):
        """
        Private constructor.
        """
        super().__init__("COLLECT_ORG_REPOS", context, github_api)

    @staticmethod
    def initialize(context, github_api):
        """
        Create instance.
        :param context: application context
        :param github_api: GitHub API wrapper
        :return:
        """
        return JobCollectOrgRepos(context, github_api)

    def _execute_task(self):
        """
        Override - define tasks of this job.
        """
        repos = self._github_api.collect_org_repos()
        self._write_to_json_file(consts.CONTRIBUTIONS_FILENAME, repos)


class JobCollectOrgMembers(Job):

    def __init__(self, context, github_api):
        """
        Private constructor.
        """
        super().__init__("COLLECT_ORG_MEMBERS", context, github_api)

    @staticmethod
    def initialize(context, github_api):
        """
        Create instance.
        :param context: application context
        :param github_api: GitHub API wrapper
        """
        return JobCollectOrgMembers(context, github_api)

    def _execute_task(self):
        """
        Override - define tasks of this job.
        """
        members = self._github_api.collect_org_members()
        self._write_to_json_file(consts.PEOPLE_FILENAME, members)
