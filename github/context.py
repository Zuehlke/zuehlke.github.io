class Context:

    def __init__(self):
        self._config = {}
        self._github_token = {}
        self._source_repo_root = ""
        self._workdir_repo_root = ""
        self._remote_url = ""

    def set_config(self, config):
        self._config = config

    def get_config(self, key):
        return self._config[key]

    def set_github_token(self, token):
        self._github_token = token

    def get_github_token(self):
        return self._github_token

    def set_source_repo_root(self, source_repo_root):
        self._source_repo_root = source_repo_root

    def get_source_repo_root(self):
        return self._source_repo_root

    def set_workdir_repo_root(self, workdir_repo_root):
        self._workdir_repo_root = workdir_repo_root

    def get_workdir_repo_root(self):
        return self._workdir_repo_root

    def set_remote_url(self, remote_url):
        self._remote_url = remote_url

    def get_remote_url(self):
        return self._remote_url
