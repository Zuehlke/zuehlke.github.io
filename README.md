# Zuehlke Github.io
The source code for the [zuehlke.github.io](http://zuehlke.github.io/) page.

## Usage
### Branches
During development, the default branch is `revitalize`. Development is done on `topic/*` and/or `feature/*` branches,
which are squash-merged back to `revitalize` when done. Once the revitalized version is merged into the mainline
repository, the default branch will be `development`. The `master` branch contains only the build, which is served on
[zuehlke.github.io](http://zuehlke.github.io/). 

### Development
- Run `npm install` to install all dependencies
- Run `npm start` to open the app in a local development server ([http://localhost:3000/](http://localhost:3000/))
- Run `npm run build` to create a production build in the `build` directory
- Run `npm run test` to run all tests (no tests defined at the moment)

### Deployment
The deployment process is yet to be defined. Most likely, it will include a Travis job that triggers on every push
to the `develop` branch, builds the application (`npm install && npm run build`) and automatically commits the contents
of the `build` directory to the master branch. Currently, the `zuehlke.github.io` repository is set up to serve the
contents on its master branch as the web page.

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
- **Add a workflow which builds the app on every push to the `develop` branch**
- **Make sure this "source branch = target branch" paradigm doesn't get too finicky, or change it if possible**
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
