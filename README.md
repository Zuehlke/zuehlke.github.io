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
- Run `npm install` to install all dependencies
- Run `npm start` to open the app in a local development server ([http://localhost:3000/](http://localhost:3000/))
- Run `npm run build` to create a production build in the `build` directory
- Run `npm run test` to run all tests (no tests defined at the moment)

## Deployment and Automation
### CI/CD
On every push to the `develop` branch, the `[push] Build and Deploy` GitHub Actions workflow is triggered, which is
defined in [.github/workflows/build-and-deploy.yml](.github/workflows/build-and-deploy.yml). This workflow checks out
the `develop` branch, builds the application using `npm run build` and commits the contents of the `build` directory
to the `gh-pages` branch.

Its final step in the `build_and_deploy` job uses the `PAT` secret, which is the Personal Access Token (PAT) of any
GitHub user with read permissions to this repository and write permissions to at least the `gh-pages` branch. It would
alternatively be possible to use `${{ secrets.GITHUB_TOKEN }}` for the GITHUB_TOKE

TODO:
- automatic build and deployment on push to develop branch, deployed to gh-pages branch
- scheduled job once a day fetches latest people and contributors from API and creates an auto-commit into the
  develop branch (which triggers another re-deploy). At the core of this workflow is a custom GitHub action (see below).
- "costs" action minutes to run
- scheduled job takes about 2.5 minutes to run at the moment
- scheduled job always operates (i.e. takes action source from and pushes to) default branch (here: develop)
- scheduled jobs can often be significantly delayed (seen up to 20 minutes late)
- data and last update in src/data

```yml
on:
  schedule:
    - cron: '0 14,15 * * *'

name: "[schedule] Update from API"

jobs:
  data_update:
    runs-on: ubuntu-latest
    name: Update data from API
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Update data from API
        uses: ./.github/actions/data-update
        with:
          github_pat: ${{ secrets.PAT }}
          data_dir: /github/workspace/src/data
      - name: Commit & push
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "[AUTO] Update data."
          file_pattern: "src/data/*.json src/data/last_update"
```

```yml
on:
  push:
    branches:
      - revitalize

name: "[push] Build and Deploy"

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2.3.1
        with:
          persist-credentials: false
      - name: npm install and run build
        run: |
          npm ci
          npm run build
      - name: Deploy build to gh-pages branch
        uses: JamesIves/github-pages-deploy-action@3.7.1
        with:
          GITHUB_TOKEN: ${{ secrets.PAT }}
          BRANCH: gh-pages
          FOLDER: build
          CLEAN: true
```
  
### Data Update Action
- Python script
- Job architecture
- constants for settings

### Resources
- Dummy GitHub user
- Specify Dummy GitHub user's PAT as an input to the custom action (used for API access only)

## Architecture
This application is built with React and is managed through
[create-react-app](https://www.npmjs.com/package/create-react-app).

### Pages
- `Contributions`: TBD (most likely, repos owned or contributed to by the Zühlke org)
- `Spotlight`: TBD (most likely, manually added repos owned or contributed to by Zühlke employees' personal accounts)
- `People`: TBD, related to contributors to repos in `Contributions` and `Spotlight`

### Components
- `Hero`: The hero image with the Zühlke open source mission statement. This component should only be used across the
  full document width.
  
## Improvements and Additional Features
### Frontend
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
- **Implement a reliable scheduled trigger for the automation workflow**
- **Update documentation**
  - Doc comments in code
  - Custom action
  - Workflows
  - Limitations due to GitHub Actions (2000 minutes / month quota for the account, script takes longer with every new user in the Zühlke org)
  - Reson why we went with custom Action vs. Web App on Azure
  - Trigger
  - Special users, permissions, tokens, etc.
  - Overall architecture
  - Expectations for data coming from GitHub API (only showing non-concealed members (althoug that should theoretically be different, according to the API specs), alumni are still members, etc.)
- Migrate to JavaScript
  - We currently spend about 1 minute per run on a Docker build
  - Regular GitHub Action environment provides everything we need, except for a Python runtime: if we use JavaScript, we don't need Docker anymore
  - When not using Docker, make sure to commit all `node_modules` - there is no `npm intall` step. Be careful not to accidentally `.gitignore` some file or directory in the `node_modules` (e.g. some `dist` dir).
- Implement commit / push logic, rather than using a third-party action (for security and to reduce dependencies)
  - Big parts of the logic already exist in Python, up until commit `???`
  - Note: That code is not up-to-date with the current setup and architecture, many concepts have changed (context, config file, workdir / source dir, etc.)
  - Need a way to either use a GitHub PAT for pushing, or pass an SSH key into the action
- Consider other deployment strategies
  - (Container App or something)
  - Azure Function
  - Azure Web App on an F1 or B1 tier App Service Plan (need to either not use Docker, or also pay for a container registry)
