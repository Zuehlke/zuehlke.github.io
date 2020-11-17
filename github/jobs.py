import json
import log


class Job:

    def __init__(self, job_name, context, github_api):
        self._job_name = job_name
        self._context = context
        self._github_api = github_api

    def _write_to_json_file(self, filename, data):
        out_dir_path = self._context.get_workdir_data_dir_path()
        filepath = out_dir_path.joinpath(filename)
        try:
            with open(filepath, "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=2)
        except FileNotFoundError:
            log.abort_and_exit("JOBS", f"Output directory path '{out_dir_path}' not found.")

    def run(self):
        log.info("JOBS", f"Starting job '{self._job_name}'.")
        self._execute_task()
        log.info("JOBS", f"Completed job '{self._job_name}'.")

    def _execute_task(self):
        raise NotImplementedError


class JobCollectOrgRepos(Job):

    def __init__(self, context, github_api):
        super().__init__("COLLECT_ORG_REPOS", context, github_api)

    @staticmethod
    def initialize(context, github_api):
        return JobCollectOrgRepos(context, github_api)

    def _execute_task(self):
        repos = self._github_api.collect_org_repos()
        self._write_to_json_file(self._context.get_config("contributions_filename"), repos)


class JobCollectOrgMembers(Job):

    def __init__(self, context, github_api):
        super().__init__("COLLECT_ORG_MEMBERS", context, github_api)

    @staticmethod
    def initialize(context, github_api):
        return JobCollectOrgMembers(context, github_api)

    def _execute_task(self):
        members = self._github_api.collect_org_members()
        self._write_to_json_file(self._context.get_config("people_filename"), members)
