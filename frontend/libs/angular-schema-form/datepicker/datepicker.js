'use strict';

angular.module('schemaForm')
// Requires the following libraries:
//    jQuery, bootstrap.js, moment.js and Eonasdan/bootstrap-datetimepicker
//
// Usage:
// $scope.form = [
//     {
//         "key": 'bday',
//         "type": 'datepicker',
//         "dateFormat": 'MM/DD/YYYY'
//     },
//
//     // Without date format, this will become in this pattern
//     // 03/19/2015 5:38 PM
//     {
//         "key": 'bday_event',
//         "type": 'datepicker'
//     }
// ];
// $scope.schema = {
//     "type": "object",
//     "title": "Info",
//     "properties": {
//         "bday": {
//             "type": "string",
//             "title": "Birthday"
//         },
//         "bday_event": {
//             "type": "string",
//             "title": "Birthday Event"
//         }
//     },
//     "required": []
// };
    .run(['$templateCache',
        function ($templateCache) {
            $templateCache.put('datepicker.html',
                    '<div class="form-group" ng-class="{\'has-error\': hasError(), \'has-success\': hasSuccess()}">' +
                    '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                    '   <div class="input-group" style="width: 100%">' +
                    '       <input ng-show="[[form.key]]"' +
                    '           type="text" style="border-radius: 3px"' +
                    '           class="form-control"' +
                    '           schema-validate="form"' +
                    '           ng-model="$$value$$"' +
                    '           datetime-picker="[[form.dateFormat]]"' +
                    '           datepicker-options="{showWeeks: false}"' +
                    '           datepicker-append-to-body="true"' +
                    '           placeholder="[[ form.placeholder ]]"' +
                    '           picker-type="[[ form.picker_type ]]"' +
                    '           ' +
                    '            />' +
                    '   <div>' +
                    '   <span class="help-block">[[hasError() ? form.description : ""]]</span>' +
                    '</div>');
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var datepicker = function (name, schema, options) {
                if (schema.type === 'datepicker') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'datepicker';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(datepicker);

            //Add to the bootstrap directive
            schemaFormDecoratorsProvider
                .addMapping('bootstrapDecorator',
                'datepicker',
                'datepicker.html');
            schemaFormDecoratorsProvider
                .createDirective('datepicker',
                'datepicker.html');
        }]);