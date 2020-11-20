# GitHub Automation
## Usage
- Check the config file (`conf/config.json`) and make sure all settings are correct.
- Run `pip install -r requirements.txt` (preferably in a `virtualenv` environment) from within this directory to
  install the required dependencies.
- Run `main.py` with Python 3, and with the required GitHub API token environment variable set. The name of this
  variable is defined in `config.json`. 

### Example Usage
```
GITHUBAPI_TOKEN=<some_api_token> python3 automation.py 
```

### Source Repo and Workdir
Part of the automation process includes creating automated commits and pushes. These actions are performed on a
secondary clone of the repository that includes the automation script, which is referred to as the _working directory_
or the _workdir_. The name of the workdir is set in the config file, and its location is always next to the source
repository. The workdir is not deleted after the script execution.

To determine the URL of the remote to be used for the workdir, the script retrieves the URL of a remote of its
containing source repository. The name of the remote to be used for this is set in the config file. For example: if
the target remote is configured to `origin` and the URL of the `origin` remote of the current repository is
`git@github.com:Example/example`, that URL is used for creating the workdir clone (if necessary) and for pushing
any new changes.

Most git operations such as `checkout`, `commit` and `push` are only ever performed on the workdir, to avoid changing
the source code of the script itself. The only "active" operation performed on the source repository is a `git pull`
at the start of the script, which allows it to receive updates to the config file.

**Warning**: Do not use this automatic pull mechanism to update the script itself. The script is not restarted after the
pull, which may lead to undefined behavior of some parts of it are updated during execution.

### Script Lifecycle
When the script is executed, it performs the following steps:
- Pull the source repository (i.e. the repository in which the script is located).
- Ensure that a second clone of the same repository exists, which will be used as a working directory. This second clone
  is always located next to the source repo. Its name is set in the config file.
- Fetch and prune the workdir repo.
- Check out the target branch in the workdir repo, as specified in the config file.
- If the target branch is tracked on the remote (specified in the config file), pull that branch.
- Run the main jobs. This includes fetching org members and repositories and updating the respective data files
  (specified in the config file) in the workdir.
- Commit changes in the workdir to its current branch, if there is anything to commit.
- Push the workdir's current branch if there was a commit, or if the `push_always` config option is set.

### Additional Information
A log file is automatically created in the present working directory. To change the logging behavior, run `main.py -h`
for more information.

Git and API operations are generally implemented in a "fail-safe" manner. That is, an unexpected status or response
will usually cause the script to error out and terminate, in order to avoid data corruption or excessive use of a
third-party API.

### Config File
The config file has the following properties:
- `remote_name`: The name of the git remote with which to interact (usually `origin`).
- `workdir_root_name`: Directory name of the second repository clone (sibling of this repository directory) which serves
  as a workspace for the script.
- `target_branch`: Name of the branch which this script should work on.
- `no_commit`: Do not commit and/or push the workdir repository.
- `push_always`: Always push target branch, even if there are no new commits (ensures branch is tracked), unless
  `no_commit` is set to `true`.
- `github_api_token_envvar`: Name of the environment variable through which the GitHub API token is provided.
- `rate_limit_buffer_sec`: Wait this many additional seconds before retrying after a rate limit should have been lifted.
- `request_delay_sec`: Wait this many seconds between requests (to avoid abuse rate limiting),
- `rate_limit_max_age_sec`: The latest rate limit status can be this many seconds old before it is considered stale.
- `max_retries`: The maximum number of times a failed request is retried (includes failures due to rate limiting)
- `data_dir_path`: Path segments to the data output directory, relative to repository root.
- `contributions_filename`: Name of the contributions data file.
- `people_filename`: Name of the people data file.

## JSON Reducer DSL
API responses usually contain much more information than we need for our data files. The `json_reducer` helps reduce
JSON payloads to only the fields we are interested in. A call to `json_reducer.reduce()` takes two arguments: a schema
node, and a JSON node (array or object) to be reduced. The schema follows a small DSL with the following rules:
- The schema is a nested Python dictionary which has the same structure as the JSON node to be reduced.
- If a JSON child node has no corresponding node in the schema, it is discarded in the output.
- The value `{}` defines a base case in the schema, and implies that the corresponding JSON value or child node should
  be fully included in the output without further reduction.
- Arrays in the schema can either be empty or contain exactly one object.
- The value `[]` defines another base case in the schema and implies that the contents of the corresponding JSON array
  should be fully included in the output without further reduction.
- An array containing an object in the schema implies that all elements of the corresponding JSON array should be
  reduced to the structure defined by that object.

For examples, refer to `github/test/test_json_reducer.py`.
