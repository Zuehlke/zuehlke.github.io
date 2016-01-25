
# org-site
This are the sources for the zuehlke.github.io repository.

You will find all source files on the develop branch.
The master branch is only for distribution and contains the builded and minified files.

To run the application you have to install npm first

In project directory (where package.json lays) execute on console: 

1. npm install
2. bower install
3. tsd reinstall

check console logs for missing packages and try to install them with npm or bower.
If you got errors when executing "bower install" try to change to an less restrictive network (zred)
and try again.

If everything looks fine you can build and start the application (on console again) with:

1. gulp or gulp build
2. gulp serve

