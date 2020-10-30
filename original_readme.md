
# Welcome to our Zühlke Github.io Site

This are the sources for the zuehlke.github.io repository.

This Site is where we present our contributions to the Open-source community.

Everybody of the Zühlke Open Source Community who did relevant contributions to open source projects should be listed here and also all the repositories where Zühlke people did relevant substantial contributions (no matter whether owned by Zühlke or not).

## Branches

* `develop`: You find all source files here.
* `master`: is only for distribution and contains the builded and minified files.

## How to get listed under "People" and/or "Contributions"

If you want to make your contributions to Open-source Projects visible on the Zühlke github page, then just follow the following very easy steps (you do not have to checkout the repo, everything can be done in github web frontend easily!).

1. Become a Member of the Zühlke Open Source Community (if not yet):
  * Check it: Zühlke badge is publicly visible on your github profile (also when you sign out!)
  * If not yet: please follow instructions under https://github.com/Zuehlke/core/issues/6

2. Add yourself to `people` as follows (can be done in github web frontend easily):
    * Choose branch `develop`
    * Choose to edit the file [src/files/people.json](src/files/people.json) 
    * Add a json block for yourself, with the image URL of your github profile picture
    * In commit block at the bottom choose to `Create new branch and start pull request`
    * Choose a branch name with your Zühlke username
    * Select `Propose file change`
    
3. Add repositories you did substantial contributions to under `contributions` (if not yet listed):    
    * if you already opened a pull request for getting listed under people, just choose that same opened feature branch for doing the change and directly edit and commit on this same feature branch (gets added to the pull request you allready opened)
    * otherwise proceed in the same way as described above for people
    * propose a change for the file [src/files/contributions.json](src/files/contributions.json).

4. Your changes will become public after someone accepted your pull-request and merged the changes into the master branch (no automatized build yet). Currently @kabaehr is doing that.

## How to build and run

To run the application you have to install npm first

In project directory (where package.json lays) execute on console: 

```
npm install
bower install
tsd reinstall
```

check console logs for missing packages and try to install them with npm or bower.
If you got errors when executing "bower install" try to change to an less restrictive network (zred)
and try again.

If everything looks fine you can build and start the application (on console again) with:

1. gulp or gulp build
2. gulp serve

## Questions?

Write an E-Mail to github@zuehlke.com or get in touch with var, cmk, bmi or kaba.
