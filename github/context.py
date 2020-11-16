import json
import os

import log


class Context:

    def __init__(self, config, github_token, source_repo_root, workdir_repo_root, data_dir_path):
        self._config = config
        self._github_token = github_token
        self._source_repo_root = source_repo_root
        self._workdir_repo_root = workdir_repo_root
        self._data_dir_path = data_dir_path

    @staticmethod
    def _read_config_file(main_script_path):
        file_path = main_script_path.parent.joinpath("config.json")
        try:
            with open(file_path) as infile:
                return json.load(infile)
        except FileNotFoundError:
            log.abort_and_exit("CTXT", f"Context init failed, could not to read config file '{file_path}': not found.")

    @staticmethod
    def _read_env_var(var_name):
        val = os.getenv(var_name)
        if val is None:
            log.abort_and_exit("CTXT", f"Context init failed, required env var '{var_name}' is not defined.")
        return val

    @staticmethod
    def initialize(main_script_path):
        config = Context._read_config_file(main_script_path)
        github_token = Context._read_env_var(config["github_api_token_envvar"])
        source_repo_root = main_script_path.parent.parent
        workdir_repo_root = source_repo_root.parent.joinpath(config["workdir_root_dirname"])
        data_dir_path = workdir_repo_root.joinpath(*config["data_dir_path"])
        return Context(config, github_token, source_repo_root, workdir_repo_root, data_dir_path)

    def get_config(self, key):
        return self._config[key]

    def get_github_token(self):
        return self._github_token

    def get_source_repo_root(self):
        return self._source_repo_root

    def get_workdir_repo_root(self):
        return self._workdir_repo_root

    def get_workdir_data_dir_path(self):
        return self._data_dir_path
