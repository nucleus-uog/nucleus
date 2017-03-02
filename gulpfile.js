// Package
var fs = require('fs');
var pkg = JSON.parse(fs.readFileSync('./package.json'));

// Gulp
var gulp = require('gulp');


// Plugins
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var gulpIf = require('gulp-if');
var imagemin = require('gulp-imagemin');
var cache = require('gulp-cache');
var runSequence = require('run-sequence');
var cleancss = require('gulp-clean-css');
var concat = require('gulp-concat');
var autoprefixer = require('gulp-autoprefixer');
var del = require('del');
var watch = require('gulp-watch');

// Build
gulp.task('build:css', function(){
  return gulp.src([pkg.settings.src.css, "./node_modules/bootstrap/dist/css/bootstrap.min.css"])
    .pipe(sass())
    .pipe(concat(pkg.settings.filenames.css))
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }))
    .pipe(cleancss())
    .pipe(gulp.dest(pkg.settings.out.css));
});

gulp.task('build:js', function(){
  return gulp.src([pkg.settings.src.js,
                   "./node_modules/jquery/dist/jquery.js",
                   "./node_modules/tether/dist/js/tether.js",
                   "./node_modules/bootstrap/dist/js/bootstrap.js"])
    .pipe(concat(pkg.settings.filenames.js))
    .pipe(uglify())
    .pipe(gulp.dest(pkg.settings.out.js));
});

gulp.task('build:images', function(){
    return gulp.src(pkg.settings.src.images)
               .pipe(imagemin())
               .pipe(gulp.dest(pkg.settings.out.images));
});

gulp.task('build:templates', function(){
    return gulp.src(pkg.settings.src.templates)
               .pipe(gulp.dest(pkg.settings.out.templates));
});

gulp.task('build', ['build:css', 'build:js', 'build:images', 'build:templates'], function(){});


// Clean

gulp.task('clean:css', function() {
  return del.sync(pkg.settings.out.css);
});

gulp.task('clean:templates', function(){
  return del.sync(pkg.settings.out.templates);
});

gulp.task('clean:js', function(){
  return del.sync(pkg.settings.out.js);
});

gulp.task('clean:images', function(){
  return del.sync(pkg.settings.out.images);
});

gulp.task('clean', ['clean:css', 'clean:templates', 'clean:js', 'clean:images'], function(){});

// watch
gulp.task('watch', function(){
    runSequence('clean', 'build');

    // CSS
    watch([
        pkg.settings.src.css
    ], (events) => {
        runSequence('clean:css', 'build:css');
    });

    // JS
    watch([
        pkg.settings.src.js
    ], (events) => {
        runSequence('clean:js', 'build:js');
    });

    // Images
    watch([
        pkg.settings.src.images
    ], (events) => {
        runSequence('clean:images', 'build:images');
    });

    // Templates
    watch([
        pkg.settings.src.templates
    ], (events) => {
        runSequence('clean:templates', 'build:templates');
    });
});

gulp.task('default', ['watch']);
