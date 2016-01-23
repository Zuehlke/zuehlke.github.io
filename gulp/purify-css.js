'use strict';

var gulp = require('gulp');

var $ = require('gulp-load-plugins')();

var paths = gulp.paths;

var purify = require('gulp-purifycss');

gulp.task('purify', function() {
    return gulp.src('./src/sass/index.css')
        .pipe(purify([ paths.src + '/{app,components}/**/*.js', paths.src + '/{app,components}/**/*.html']))
        .pipe(gulp.dest(paths.src + '/sass/pur/'));
});

