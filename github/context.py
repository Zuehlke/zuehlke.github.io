import json
import os

import log


class Context:
    """
    Represents an application context containing shared information such as configurations, paths and secrets.
    """

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
            log.abort_and_exit("CTXT", f"Context init failed, required env var '{var_name}' is not set.")
        return val

    @staticmethod
    def create(main_script_path):
        """
        Create a new Context.
        :param main_script_path: absolute pathlib.Path to the main script.
        :return: newly created Context object
        """
        config = Context._read_config_file(main_script_path)
        github_token = Context._read_env_var(config["github_api_token_envvar"])
        source_repo_root = main_script_path.parent.parent
        workdir_repo_root = source_repo_root.parent.joinpath(config["workdir_root_dirname"])
        data_dir_path = workdir_repo_root.joinpath(*config["data_dir_path"])
        return Context(config, github_token, source_repo_root, workdir_repo_root, data_dir_path)

    def get_config(self, key):
        """
        Get a config value for a given key, corresponding to the config.json file.
        :param key: key of the config value
        :return: config value at the specified key, or None of key doesn't exist
        """
        return self._config.get(key)

    def get_github_token(self):
        """
        Get the GitHub API token.
        :return: GitHub API token.
        """
        return self._github_token

    def get_source_repo_root(self):
        """
        Get the absolute pathlib.Path to the root of the repository which contains the main script.
        :return: absolute root path to the source repository
        """
        return self._source_repo_root

    def get_workdir_repo_root(self):
        """
        Get the absolute pathlib.Path to the root of the repository which is used as the working directory.
        :return: absolute root path to the workdir repo
        """
        return self._workdir_repo_root

    def get_workdir_data_dir_path(self):
        """
        Get the absolute pathlib.Path to the workdir subdirectory which should contain all data outputs.
        :return: absolute path to the data output directory in the workdir
        """
        return self._data_dir_path
