'use strict';

var gulp = require('gulp');

var paths = gulp.paths;

var $ = require('gulp-load-plugins')();

var sprite = require('sprity').stream;

  var pngFilter = $.filter('*.png');
  var scssFilter = $.filter('**/*.scss');
// generate sprite.png and _sprite.scss
gulp.task('sprites', function () {
   return gulp.src(paths.src + '/sass/icons/*.png')
    .pipe(sprite({
      name: 'sprite',
      style: '_sprite.scss',
      cssPath: './assets/images/',
      processor: 'scss',
      retina: true      
    }))
    .pipe(pngFilter)
    .pipe(gulp.dest(paths.src + '/assets/images/'))
    .pipe(pngFilter.restore())
    .pipe(scssFilter)
    .pipe(gulp.dest(paths.src + '/sass/'))
    .pipe(scssFilter.restore())
    .on('error', function handleError(err) {
      console.error(err.toString());
      this.emit('end')
    });
});

gulp.task('styles', function () {

  var sassOptions = {
    style: 'expanded'
  };

  var injectFiles = gulp.src([
    paths.src + '/sass/**/*.scss',
    '!' + paths.src + '/sass/index.scss'
  ], { read: false });

  var injectOptions = {
    transform: function(filePath) {
      filePath = filePath.replace(paths.src + '/sass/', '');
      return '@import \'' + filePath + '\';';
    },
    starttag: '// injector',
    endtag: '// endinjector',
    addRootSlash: false
  };

  var indexFilter = $.filter('index.scss');

  return gulp.src([
    paths.src + '/sass/index.scss'
  ])
    .pipe(indexFilter)
    .pipe($.inject(injectFiles, injectOptions))
    .pipe(indexFilter.restore())
    .pipe($.sass(sassOptions))

  .pipe($.autoprefixer())
    .on('error', function handleError(err) {
      console.error(err.toString());
      this.emit('end');
    })
    .pipe(gulp.dest(paths.tmp + '/serve/app/'));
});
