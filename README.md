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
