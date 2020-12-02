# Zuehlke Github.io
The source code for the [zuehlke.github.io](http://zuehlke.github.io/) page.

## Usage
### Branches
The default branch is `development`. All changes should be made via pull requests into that branch. The `gh-pages`
branch contains only the build, which is served on [zuehlke.github.io](http://zuehlke.github.io/). A build and
re-deployment is automatically triggered on every push to the `develop` branch (see "Deployment and Automation" below).
The `master` branch contains the last build of the old application, which is no longer being served.

**In summary:**
- `development`: default branch, pushes to this branch trigger a build and re-deployment
- `gh-pages`: deployed branch containing the static web page
- `master`: no longer in use, contains the latest build of the old website

### Development
**Web application**
- Run `npm install` to install all dependencies
- Run `npm start` to open the app in a local development server ([http://localhost:3000/](http://localhost:3000/))
- Run `npm run build` to create a production build in the `build` directory
- Run `npm run test` to run all tests (no tests defined at the moment)

**Automation**
- In `.github/actions/data-update`, run `pip install -r requiremets.txt`, preferably in a `virtualenv` environment
- To execute the script, run `INPUT_GITHUB_PAT=<PAT_PUBLIC> INPUT_DATA_DIR=<some_dir> python src/main.py`

where

- `PAT_PUBLIC` is a public-access-only GitHub PAT (see _Resources_)
- `some_dir` is the absolute path to the desired data output directory (usually, the `src/data` subdirectory of a clone
  of this repository)

## Frontend Structure
The frontend is written in React + TypeScript and is managed through
[create-react-app](https://www.npmjs.com/package/create-react-app). It has the following pages:
- `Contributions`: All public repositories owned by the Zühlke organization. 
- `People`: All non-concealed members of the Zuehlke organization. This may include Zühlke alumni who are still actively
  contributing to Zuehlke repositories. Organization membership is managed by Ben Millo.
  
The data for these two pages are loaded client-side from `src/data/contributions.json` and `src/data/people.json`
respectively. These files are automatically generated by the `data-update` GitHub action (see _Data Update Automation_)
and contain publicly available data fetched from the GitHub API, such as a repository's name, description and stargazer
count, and a person's GitHub name, full name, bio and avatar.

The website is mobile-responsive and its design approximates that of the
[Zühlke corporate page](https://www.zuehlke.com/en).

## Deployment and Automation
### GitHub Pages
[GitHub Pages](https://pages.github.com/) is a feature offered by GitHub which allows every user or organization to
serve the contents of one repository as a static website. The name of that repository has to be
`<user_or_org>.github.io`, which will also be the default URL for the resulting web page. In our case, this is
`zuehlke.github.io`, and [http://zuehlke.github.io](http://zuehlke.github.io) respectively.

In the settings for a GitHub Pages repository, we can specify the branch which should be served as the website. In our
case, the branch to be served is set to `gh-pages`. It therefore needs to contain the built, static website content,
rather than any source code. A GitHub Actions workflow is set up to automatically build the application on every push
to the `develop` branch and commit the results to the `gh-pages` branch (see _CI/CD_).

### CI/CD
On every push to the `develop` branch, the `[push] Build and Deploy` GitHub Actions workflow is triggered, which is
defined in [.github/workflows/build-and-deploy.yml](.github/workflows/build-and-deploy.yml). This workflow checks out
the `develop` branch, builds the application using `npm run build` and commits the contents of the `build` directory
to the `gh-pages` branch.

The `secrets.GITHUB_TOKEN` value used in the `build_and_deploy` job's final step is a special environment variable
automatically provided to every GitHub Actions workflow. This token grants the workflow full permissions on the
repository it is running for.

This workflow can also be manually triggered in the repository's _Actions_ tab. Make sure to select the branch with the
most up-to-date workflow description (i.e. `build-and-deploy.yml` file) (usually the default branch, `develop`).

### Data Update Automation (Workflow)
- `[schedule] Update from API` workflow, defined by
  [.github/workflows/update-from-api.yml](.github/workflows/update-from-api.yml) (file contains additional
  documentation).
- A scheduled workflow which runs once a day.
  - Note: Scheduled execution is often significantly delayed (can be 30 minutes or more).
  - Schedule is defined as a cron expression in the `update-from-api.yml` file.
- Can also be manually triggered in the repository's _Actions_ tab. Make sure to select the branch with the most
  up-to-date workflow description (i.e. `update-from-api.yml` file) (usually the default branch, `develop`).
- When triggered by schedule, the relevant workflow definition is the one present on the default branch
  (here, `develop`).
- Fetches the latest people and contributors data from API and creates an auto-commit into a working branch.
- API access and data update is handled by a custom GitHub action (see _Custom Action_ below).
- Working branch:
  - Is specified in the `with.ref` field for the workflow's `Checkout` step.
  - Defines both the source branch for the custom action source code, and the target branch for the automated commit.
  - Is currently set to `develop`. Hence, the automated push will also trigger a re-build of the application into the
    `gh-pages` branch.
- The custom action step takes two inputs: `github_pat` and `data_dir`.
  - Both are automatically passed as environment variables to the Docker container running the script
  - Environment variables coming from inputs follow the naming pattern `INPUT_<INPUT_NAME>`. Hence, these two inputs
    will be become environment variables called `INPUT_GITHUB_PAT` and `INPUT_DATA_DIR` respectively, from the point
    of view of the custom action Python script.
  - The `data_dir` input is set to `/github/workspace/src/data`. The `actions/checkout@2` action clones the
    current repository into a location which is bind-mounted to `/github/workspace/` in the Docker container.
- This workflow definitions requires two separate GitHub PATs to be defined in the repository's Secrets:
  - `PAT_PUBLIC`: Has public-only access. Using this PAT for the custom action ensures that API calls won't return
    private repositories or concealed organization members.
  - `PAT_PRIVATE`: Used for checking out the current repository. This token needs full access to private Org repos to
    be able to clone the repository and push to it. Note that this PAT is specifically used in the Checkout step, in
    lieu of the `secrets.GITHUB_TOKEN` provided to every workflow and used by this action by default. This is due to the
    fact that a push executed with `secrets.GITHUB_TOKEN` does not trigger any subsequent actions (e.g. building the)
    web application, nor does it count as "repository activity", which is required to avoid scheduled workflows getting
    automatically deactivated.

### Data Update Automation (Custom Action)
- A custom GitHub action which retrieves data from the GitHub API and outputs the result into specified files.
- Located in `.github/actions/data-update`.
- Implemented as dockerized python script (Python doesn't run natively on GitHub Actions).
- Inputs: see _Workflow_ documentation above.
- Entry point: `main.py`.
- Fetches all public repositories and non-concealed members of the `Zuehlke` GitHub organization.

The script can be configured in code by editing `src/consts.py`. The following parameters are available:
- `ENV_GITHUB_PAT`: Name of the environment variable which provides the GitHub PAT
- `ENV_DATA_DIR`: Name of the environment variable which provides the full path to the data output directory
- `API_REQUEST_DELAY_SEC`: Number of seconds to wait before every API request, to avoid flooding the API
- `RATE_LIMIT_BUFFER_SEC`: Number of seconds to wait after a rate limit is supposed to be lifted, to avoid overlap
- `RATE_LIMIT_MAX_AGE_SEC`: Maximum number of seconds since the rate limit update before the current rate limit status
  information is considered stale and has to be updated.
- `MAX_RETRIES`: The maximum number of retries when a request fails (also applies for failed requests due to rate
  limitation). After that, the execution fails. **Warning**: This value should be set to `0` when deploying to
  platforms with usage-based pricing (e.g. GitHub Actions), since waiting for a rate limit to be lifted will result in
  additional compute time, which can be expensive.
- `CONTRIBUTIONS_FILENAME`: Name of the contributions output file in the data output directory (file will be created or
  overwritten).
- `PEOPLE_FILENAME`: Name of the people output file in the data output directory (file will be created or overwritten).

### Resources
- **Email account:** TBA
- **Bot GitHub User:** A GitHub user with read and write permissions to this repository
  - **Username:** TBA
  - **Email:** TBA
- **PAT_REPO**: A _GitHub Personal Access Token_ (PAT) owned by the bot user's account and created with the full `repo`
  scope.
  - Created in the bot user's GitHub account, under `Settings -> Developer settings -> Personal access tokens`.
  - Added as `PAT_REPO` to this repository's _Secrets_.
- **PAT_PUBLIC**: A _GitHub Personal Access Token_ (PAT) owned by the bot user's account and created without selecting
  any scopes, resulting in public-only access to repositories, organization members, etc.
  - Created in the bot user's GitHub account, under `Settings -> Developer settings -> Personal access tokens`.
  - Added as `PAT_PUBLIC` to this repository's _Secrets_.

### Azure
The initial plan was to deploy the automation script on Azure, most likely as a Docker container with a cron job which
automatically executes the script once per day. However, this approach was discarded due to the following reasons:
- An F1-tier App Service Plan may have rate limits which are too strict for the script to run to completion
- A B1-tier App Service Plan is expensive, considering our application would be running for only about ~5 minutes / day
  and would be idling for the rest of the time
- When using Docker, we would also need to rent a container registry for an additional 5.-/month.

An Azure subscription already exists for this project:
- Name: I10ZCH_SWE6 - zuehlke github io
- Id: 53bca82e-7c7d-4a54-ab90-8e82f48a27c9
- Members: Silas Berger, Sergio Trentini
- Monthly budget declared to PSS: $15 / month

### Limitations
- GitHub Actions has a limited monthly quota of Action Minutes per account or organization. For organizations without
  a premium plan, the free tier currently includes 2000 minutes/month. The update automation and build workflow run for
  a combined total of approximately 5 minutes/day, ~150 minutes/month. These minutes count against the Zuehlke
  organization's total quota of 2000 minutes / month. Additional API requests (e.g. due to added organization members or
  due to additional data to be fetched), the automation's execution time will increase.
- According to GitHub's policies, scheduled workflows (such as the automation workflow) get automatically deactivated 
  if a repository has no activity for at least 2 months. This should be remedied in our case by letting the automation
  script perform automated commits as a reular user (by providing a PAT), but it remains to be seen whether this works
  long-term.
  
## Improvements and Additional Features
### Frontend
- **Consider using Zühlke font for H2 headings, use slightly weaker gray.**
- **Use translate instead of left for the mobile nav slide-in (should improve performance issues)**
- **Sort by relevance (stargazers, forks, watchers, activity)**
- Show stargazers / forks / watchers counts on contribution tiles
- Allow curated inputs
  - In an additional JSON file, we can add repo IDs which should be crawled even if they are not owned by the Zühlke org
    (showcase (potentially private) contributions by Zühlke employees)
  - Same for people
  - Non-Zühlke repos
  - Blacklist repos and people (e.g. avoid dummy repos, bot users or people who don't want to be featured on the
  website)
- Is there a way to connect people and repos? Maybe we could click on a person and only get their repos? Note: this
  would require requesting contributor IDs for every repo. For large projects, this could mean having to fetch a large
  number of pages (current limit: 100 results per request).
- Full-text search, filters, sorting

### Automation
- Migrate to JavaScript
  - We currently spend about 1 minute per run on a Docker build
  - The regular GitHub Action environment provides everything we need, except for a Python runtime: if we use
    JavaScript, we don't need Docker anymore.
  - There is no inherent reason to implement the automation in Python, rather than JavaScript.
  - When not using Docker, make sure to commit all `node_modules` - there is no `npm intall` step. Be careful not to
    accidentally `.gitignore` some file or directory in the `node_modules` (e.g. some `dist` dir).
- Implement commit / push logic, rather than using a third-party action (for security and to reduce dependencies)
  - Big parts of the logic were already in Python, and removed during the migration to GitHub Actions, in commit 
    [6315e486b3cceafd4918c242819b4727bec0b1ff](https://github.com/SilasBerger/zuehlke.github.io/commit/6315e486b3cceafd4918c242819b4727bec0b1ff)
    (see [git_wrapper.py](https://github.com/SilasBerger/zuehlke.github.io/commit/6315e486b3cceafd4918c242819b4727bec0b1ff)).
  - Note: That code is not up-to-date with the current setup and architecture, many concepts have changed (context,
    config file, workdir / source dir, etc.)
  - Needs to be modified to use a GitHub PAT for authentication, rather than the default SSH key available on the
    system (should be able to use
    [https://github.com/stefanzweifel/git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action)
    for reference).
- Consider other deployment strategies
  - Azure ContainerInstances
  - Azure Functions
  - Azure Web App on an F1 or B1 tier App Service Plan (need to either not use Docker, or also pay for a container
    registry)
- In case the scheduled GitHub Action workflow is does not trigger reliably or gets deactivated due to a lack of
  repository activity, consider changing the `update-from-api.yml` action's trigger to `workflow_dispatch`. The workflow
  via a `POST` request to
  `https://api.github.com/repos/Zuehlke/zuehlke.github.io/actions/workflows/update-from-api.yml/dispatches`, using the
  `PAT_REPO` token, or a different PAT with the same permission level (full private repo access).

## Integration Instructions
This section is only relevant for integrating the current forked branch into the mainline repository and can be removed
afterwards. To integrate the revitalization, the following steps are required:
- In the Zuehlke organization settings, make sure no credit card is added, or a spending limit (e.g. $0/month) is in
  place for GitHub Actions (safety precautions, in case workflows run significantly longer or more often than expected).
- Grant read/write access for `Zuehlke/zuehlke.github.io` to the Bot GitHub User.
- Create a `PAT_PUBLIC` and `PAT_REPO` (see _Resources_) in the Bot GitHub User's account and add them to the
  `Zuehlke/zuehlke.github.io` repository's _Secrets_, using these exact names.
- Merge the pull request from `SilasBerger/zuehlke.github.io@revitalize` into `Zuehlke/zuehlke.github.io@develop`.
- Make sure the _Actions_ tab shows two actions named `[push] Build and Deploy` and `[schedule] Update from API`.
  - If this is not the case, try committing a minor change to the corresponding `.yml` file (e.g. change the workflow's
    name, add a comment). This generally gets GitHub Actions to detect the added workflow.
- Manually execute the `[push] Build and Deploy` workflow on the `develop` branch, to build the application and
  deploy to the `gh-pages` branch.
- In the `Zuehlke/zuehlke.github.io` repository settings, set the `gh-pages` branch as the "deployed branch" in the
  GitHub Pages section.
- The new page should now be live and available at [http://zuehlke.github.io](http://zuehlke.github.io).
- After the first scheduled execution of the `[schedule] Update from API` workflow, check the repository's _Actions_
  tab to verify that the job ran successfully. Keep in mind that a delay between the scheduled and the actual execution
  time of up to 30 minutes is not unusual.
