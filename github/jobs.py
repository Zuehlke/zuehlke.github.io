import json
import log


class Job:

    def __init__(self, job_name, context, git_wrapper, github_api):
        self._job_name = job_name
        self._context = context
        self._git_wrapper = git_wrapper
        self._github_api = github_api

    def _write_to_json_file(self, filename, data):
        filepath = self._context.get_workdir_data_dir_path().joinpath(filename)
        with open(filepath, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=2)

    def run(self):
        log.info("JOBS", f"Starting job '{self._job_name}'.")
        self._execute_task()
        log.info("JOBS", f"Completed job '{self._job_name}'.")

    def _execute_task(self):
        raise NotImplementedError


class JobCollectOrgRepos(Job):

    def __init__(self, context, git_wrapper, github_api):
        super().__init__("COLLECT_ORG_REPOS", context, git_wrapper, github_api)

    @staticmethod
    def initialize(context, git_wrapper, github_api):
        return JobCollectOrgRepos(context, git_wrapper, github_api)

    def _execute_task(self):
        repos = self._github_api.collect_org_repos()
        self._write_to_json_file(self._context.get_config("contributions_filename"), repos)
