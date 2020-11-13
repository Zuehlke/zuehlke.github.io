# GitHub Automation
## Usage
- Check the config file (`conf/config.json`) and make sure all settings are correct.
- Add a file called `secrets.json` to the `conf` directory (next to `config.json`) and edit it to follow the structure
  outlined in the "Secrets File" section below. This file is ignored by Git.
- Run `automation.py` with Python 3, and with the required GitHub API token env var set (var name specified in
  `config.json`). E.g:

```
GITHUBAPI_TOKEN=someAPItoken python3 automation.py 
```

### Config File
The config file has the following properties:
- `remote_name`: The name of the git remote with which to interact (usually `origin`).
- `workdir_root_name`: Directory name of the second repository clone (sibling of this repository directory) which serves
  as a workspace for the script.
- `target_branch`: Name of the branch which this script should work on.
- `github_api_token_envvar`: Name of the environment variable through which the GitHub API token is provided.
- `rate_limit_buffer_sec`: Wait this many additional seconds before retrying after a rate limit should have been lifted.
- `request_delay_sec`: Wait this many seconds between requests (to avoid abuse rate limiting),
- `rate_limit_max_age_sec`: The latest rate limit status can be this many seconds old before it is considered stale.
- `max_retries`: The maximum number of times a failed request is retried (includes failures due to rate limiting)
