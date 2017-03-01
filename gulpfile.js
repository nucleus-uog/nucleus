var gulp = require('gulp');

var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();
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

// browserSync

gulp.task('browserSync', function() {
  browserSync.init({
    server: {
      baseDir: 'source'
    },
  })
})

// Build

gulp.task('build:css', function(){
  return gulp.src("source/css/**/*.scss")
    .pipe(sass())
    .pipe(concat('style.min.css'))
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }))
    .pipe(cleancss())
    .pipe(browserSync.reload({
      stream: true
    }))
    .pipe(gulp.dest("static/css"));
});

gulp.task('build:js', function(){
  return gulp.src(["source/js/**/*.js",
                   "./node_modules/jquery/dist/jquery.js",
                   "./node_modules/tether/dist/js/tether.js",
                   "./node_modules/bootstrap/dist/js/bootstrap.js"])
    .pipe(concat("script.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("static/js"));
});

gulp.task('build:images', function(){
    return gulp.src('source/images/**/*.+(png|jpg|jpeg|gif|svg)')
               .pipe(imagemin())
               .pipe(gulp.dest('static/images'));
});

gulp.task('build:templates', function(){
    return gulp.src('source/templates/**/*.html')
               .pipe(gulp.dest('templates/nucleus'));
});

gulp.task('build', ['build:css', 'build:js', 'build:images', 'build:templates'], function(){});


// Clean

gulp.task('clean:css', function() {
  return del.sync('static/css');
});

gulp.task('clean:templates', function(){
  return del.sync('templates');
});

gulp.task('clean:js', function(){
  return del.sync('static/js');
});

gulp.task('clean:images', function(){
  return del.sync('static/images');
});

gulp.task('clean', ['clean:css', 'clean:templates', 'clean:js', 'clean:images'], function(){});

// watch
gulp.task('watch', function(){
    runSequence('clean', 'build');

    // CSS
    watch([
        'source/css/**/*.scss'
    ], (events) => {
        runSequence('clean:css', 'build:css');
    });

    // JS
    watch([
        'source/js/**/*.js'
    ], (events) => {
        runSequence('clean:js', 'build:js');
    });

    // Images
    watch([
        'source/images/**/*.+(png|jpg|jpeg|gif|svg)'
    ], (events) => {
        runSequence('clean:images', 'build:images');
    });

    // Templates
    watch([
        'source/templates/**/*.html'
    ], (events) => {
        runSequence('clean:templates', 'build:templates');
    });
});

gulp.task('default', ['watch']);
