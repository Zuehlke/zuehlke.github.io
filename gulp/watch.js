'use strict';

var gulp = require('gulp');

var paths = gulp.paths;

gulp.task('watch', ['inject'], function () {
  gulp.watch([
    paths.src + '/*.html',
    paths.src + '/sass/pur/**/*.scss',
    paths.src + '/sass/pur/**/*.css',
    paths.src + '/{app,components}/**/*.js',
    paths.src + '/{app,components}/**/*.ts',
    'bower.json'
  ], ['inject', 'styles']);
});
