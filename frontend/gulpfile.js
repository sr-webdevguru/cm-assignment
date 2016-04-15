var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var ngAnnotate = require('gulp-ng-annotate');

gulp.task('js', function () {
    gulp.src([
        //3rd party
        'libs/jquery/dist/jquery.min.js',
        'libs/bootstrap/dist/js/bootstrap.min.js',

        'libs/lodash/dist/lodash.compat.min.js',

        'libs/deep-diff/diff.js'
    ])
        //.pipe(sourcemaps.init())
        //.pipe(uglify())
        .pipe(concat('compiled/base.min.js'))
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('.'));


    gulp.src([
        //3rd party
        'libs/angular/angular.min.js',
        'libs/angular-resource/angular-resource.min.js',
        'libs/angular-cookies/angular-cookies.min.js',
        'libs/angular-sanitize/angular-sanitize.min.js',
        'libs/angular-input-number/number-input.min.js',

        'libs/angular-ui-router/release/angular-ui-router.min.js',
        'libs/restangular/dist/restangular.min.js',

        'libs/angular-bootstrap/ui-bootstrap.js',
        'libs/angular-bootstrap/ui-bootstrap-tpls.js',

        'libs/angular-strap/angular-strap.min.js',
        'libs/angular-strap/angular-strap.tpl.js',

        'libs/angular-translate/angular-translate.min.js',
        'libs/angular-translate/angular-translate-loader-static-files.min.js',

        'libs/angular-growl-v2/angular-growl.min.js',
        'libs/angular-google-chart/ng-google-chart.js',

        'libs/angular-leaflet-directive/dist/leaflet-omnivore.min.js',
        'libs/leaflet-dist/leaflet-src.js',
        'libs/leaflet-dist/leaflet-heat.js',
        'libs/leaflet-plugins/layer/tile/Google.js',
        'libs/angular-leaflet-directive/dist/shCore.js',
        'libs/angular-leaflet-directive/dist/shBrushJScript.js',
        'libs/angular-leaflet-directive/dist/webgl-heatmap.js',
        'libs/angular-leaflet-directive/dist/webgl-heatmap-leaflet.js',
        'libs/angular-leaflet-directive/dist/angular-leaflet-directive.js',
         'libs/angular-leaflet-directive/dist/leaflet.markercluster.js',

        'libs/angular-hotkeys/hotkeys.js',
        'libs/angular-loading-bar/build/loading-bar.min.js',
        'libs/angular-idle/angular-idle.min.js',
        'libs/ng-csv/ng-csv.js',

        'libs/angular-intercom/angular-intercom.min.js',

        'libs/tv4/tv4.js',
        'libs/angular-schema-form/ObjectPath.js',
        'libs/angular-schema-form/ng-flow-standalone.min.js',
        'libs/angular-schema-form/schema-form.js',
        'libs/angular-schema-form/bootstrap-decorator.js',
        'libs/angular-schema-form/schema-form-file-upload.min.js',
        'libs/angular-schema-form/schema-form-uiselect.min.js',
        'libs/angular-schema-form/googlemap/googlemap.js',
        'libs/angular-schema-form/image/eventjs/event.js',
        'libs/angular-schema-form/image/magnifierjs/magnifier.js',
        'libs/angular-schema-form/image/imagemodal.js',
        'libs/angular-schema-form/image/bootstrap-imagemodal.js',
        'libs/angular-schema-form/file/file.js',
        'libs/angular-schema-form/multiselect/checklist-model.js',
        'libs/angular-schema-form/multiselect/multiselect.js',
        'libs/angular-schema-form/repeater/repeater.js',
        'libs/angular-schema-form/units/distance.js',
        'libs/angular-schema-form/units/temperature.js',
        'libs/angular-schema-form/units/weight.js',
        'libs/angular-schema-form/units/altitude.js',
        'libs/angular-schema-form/units/length.js',
        'libs/angular-schema-form/units/height.js',
        'libs/bootstrap-ui-datetime-picker/dist/datetime-picker.js',
        'libs/angular-schema-form/datepicker/libs/moment-with-locales.min.js',
        'libs/angular-schema-form/datepicker/libs/bootstrap-datetimepicker.js',
        'libs/angular-schema-form/datepicker/datepicker.js',
        'libs/angular-schema-form/signature/signature_pad.min.js',
        'libs/angular-schema-form/signature/signature_pad.directive.js',

        'libs/angular-timezone/jstz.min.js',
        'libs/angular-timezone/moment-timezone-with-data.js',
        'libs/angular-timezone/moment-duration-format.js'
    ])
        //.pipe(sourcemaps.init())
        //.pipe(uglify())
        .pipe(concat('compiled/vendor.min.js'))
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('.'));

    gulp.src([
        // packaged
        'app/app.js',
        'app/**/*.js'
    ])

        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        //.pipe(uglify())
        .pipe(concat('compiled/app.min.js'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('.'));
});

gulp.task('watch', ['js'], function () {
    gulp.watch('app/**/*.*', ['js'])
});
