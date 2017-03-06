// Package
var fs = require('fs');
var pkg = JSON.parse(fs.readFileSync('./package.json'));

// Gulp
var gulp = require('gulp');

// Plugins
var autoprefixer = require('gulp-autoprefixer');
var cleancss = require('gulp-clean-css');
var concat = require('gulp-concat');
var del = require('del');
var favicons = require('gulp-favicons');
var fontAwesome = require('node-font-awesome');
var imagemin = require('gulp-imagemin');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var util = require('gulp-util');
var watch = require('gulp-watch');

// Build

gulp.task('build:css', function(){
   return gulp.src(["./node_modules/bootstrap/dist/css/bootstrap.min.css", pkg.settings.src.css])
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [fontAwesome.scssPath]
    }).on('error', sass.logError))
    .pipe(concat(pkg.settings.filenames.css))
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }))
    .pipe(cleancss())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(pkg.settings.out.css));
});

gulp.task('build:js', function(){
  return gulp.src(["./node_modules/jquery/dist/jquery.js",
                   "./node_modules/tether/dist/js/tether.js",
                   "./node_modules/bootstrap/dist/js/bootstrap.js",
                   pkg.settings.src.js])
    .pipe(sourcemaps.init())
    .pipe(concat(pkg.settings.filenames.js))
    .pipe(uglify())
    .pipe(sourcemaps.write())
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

gulp.task('build:fonts', function(){
    return gulp.src([fontAwesome.fonts, pkg.settings.src.fonts])
               .pipe(gulp.dest(pkg.settings.out.fonts));
});

gulp.task('build:favicon', function(){
    return gulp.src(pkg.settings.src.favicon)
               .pipe(favicons(pkg.settings.favicon))
               .on('error', util.log)
               .pipe(gulp.dest(pkg.settings.out.favicon));
});

gulp.task('build', ['build:css', 'build:js', 'build:images', 'build:templates', 'build:fonts', 'build:favicon'], function(){});


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

gulp.task('clean:fonts', function(){
  return del.sync(pkg.settings.out.fonts);
});

gulp.task('clean', ['clean:css', 'clean:templates', 'clean:js', 'clean:images', 'clean:fonts'], function(){});

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

    // Fonts
    watch([
        pkg.settings.src.fonts
    ], (events) => {
        runSequence('clean:fonts', 'build:fonts');
    });
});

gulp.task('default', ['watch']);
