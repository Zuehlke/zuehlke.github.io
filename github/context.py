class Context:

    def __init__(self):
        self._config = {}
        self._source_repo_root = ""
        self._workdir_repo_root = ""
        self._remote_url = ""

    def set_config(self, config):
        self._config = config

    def get_config(self):
        return self._config

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
