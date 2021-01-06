import json
from datetime import datetime

import consts
import log
import util
from csv import DictReader


class Job:
    """
    Represents an automation job which may involve data collection, data provisioning and file writes. A
    job does not include any Git operations such as committing or pushing.
    """

    def __init__(self, job_name, context):
        """
        Private constructor.
        :param job_name: display name of the job
        :param context: application context
        """
        self._job_name = job_name
        self._context = context

    def _write_to_file(self, filename, text):
        """
        Write text into a file in the predefined output directory.
        :param filename: name of the file (no path), should end in .json
        :param text: JSON-serializable object
        """
        out_dir_path = self._context.get_data_dir_path()
        filepath = out_dir_path.joinpath(filename)
        log.info(self._job_name, f"Writing string to {filepath}")
        try:
            with open(filepath, "w", encoding="utf-8") as outfile:
                outfile.write(text)
        except FileNotFoundError:
            log.abort_and_exit(self._job_name, f"Output directory path '{out_dir_path}' not found.")

    def _write_to_json_file(self, filename, data):
        """
        Write data into a file in the predefined output directory.
        :param filename: name of the file (no path), should end in .json
        :param data: JSON-serializable object
        """
        out_dir_path = self._context.get_data_dir_path()
        filepath = out_dir_path.joinpath(filename)
        log.info(self._job_name, f"Writing data to {filepath}")
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
        super().__init__("COLLECT_ORG_REPOS", context)
        self._github_api = github_api

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

class JobCollectExternalRepos(Job):

    def __init__(self, context, github_api):
        """
        Private constructor.
        """
        super().__init__("COLLECT_EXTERNAL_REPOS", context)
        self._github_api = github_api
        self._input = self.read_input()

    def read_input(self):
        filepath = '../input/external_contributions.csv'
        with open(filepath, 'r') as read_obj:
            log.info(self._job_name, f"Reading input from {filepath}")
            reader = DictReader(read_obj)
            return list(reader)

    @staticmethod
    def initialize(context, github_api):
        """
        Create instance.
        :param context: application context
        :param github_api: GitHub API wrapper
        :return:
        """
        return JobCollectExternalRepos(context, github_api)

    def _execute_task(self):
        """
        Override - define tasks of this job.
        """
        repos = self._github_api.collect_external_contributions(self._input)
        self._write_to_json_file(consts.EXTERNAL_CONTRIBUTIONS_FILENAME, repos)


class JobCollectOrgMembers(Job):

    def __init__(self, context, github_api):
        """
        Private constructor.
        """
        super().__init__("COLLECT_ORG_MEMBERS", context)
        self._github_api = github_api

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


class JobWriteLastUpdate(Job):

    def __init__(self, context):
        """
        Private constructor.
        """
        super().__init__("WRITE_LAST_UPDATE", context)

    @staticmethod
    def initialize(context):
        """
        Update the last_update file in the data dir with the current time and date.
        """
        return JobWriteLastUpdate(context)

    def _execute_task(self):
        """
        Override - define tasks of this job.
        """
        timestamp = f"{datetime.utcnow().strftime(util.get_time_format_pattern())} UTC+0"
        self._write_to_file("last_update", timestamp)
