'use strict';

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            var schemaHtml =
                '<div class="form-inline" style="margin-bottom:15px;">' +
                '<div class="form-group" ng-class="{\'has-error\': hasError(), \'has-success\': hasSuccess(), \'has-feedback\': form.feedback !== false}" ng-show="form.key">' +
                '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                '   <div>' +
                '       <input type="number" class="form-control" name="[[ form.key.slice(-1)[0] ]]" min="[[ form.min ]]" max="[[ form.max ]]" temperature schema-validate="form" ng-model="$$value$$" ng-pattern="/^(\\-)?[0-9]{1,4}(\\.[0-9]+)?$/">' +
                '   </div>' +
                '</div>' +
                '<div  class="form-group" style="margin:15px 0 0 15px;">' +
                '   <label class="control-label"></label>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_temperature" value="0" ng-model="form.unit"> &deg;F</label>' +
                '   </div>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_temperature" value="1" ng-model="form.unit"> &deg;C</label>' +
                '   </div>' +
                '   </div>' +
                '</div>';
            '</div>';

            $templateCache.put('temperature.html', schemaHtml);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var temperature = function (name, schema, options) {
                if (schema.type === 'temperature') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'temperature';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(temperature);

            schemaFormDecoratorsProvider.addMapping(
                'bootstrapDecorator',
                'temperature',
                'temperature.html'
            );

            schemaFormDecoratorsProvider.createDirective(
                'temperature',
                'temperature.html'
            );
        }])
    .directive('temperature',
    ['$http', '$parse', function ($http, $parse) {
        return {
            restrict: 'A',
            require: 'ngModel',

            link: function (scope, element, attrs, ngModel) {
                function F2C(value) {
                    return (value -32)/1.8;
                }

                function C2F(value) {
                    return (value * 1.8 + 32);
                }


                function initialize() {
                    var unit_scope = angular.element(element.parent().parent().parent().find("input[type=radio]").get(0)).scope();
                    var initial_unit = unit_scope.form.unit;

                    // => view -> model => model always keep "metric" value
                    ngModel.$parsers.push(function (viewValue) {
                        var modelValue = parseFloat(viewValue); //set to defined unit
                        if (unit_scope.form.unit == '0') { //imperial
                            return parseFloat((F2C(modelValue)).toFixed(1));
                        } else {
                            return parseFloat((modelValue).toFixed(1));
                        }
                    });

                    unit_scope.form.unit = '1'; // set to metric (saved unit)
                    // now model and view values are same

                    //set up watch
                    unit_scope.$watch('form.unit', function (unit) {
                        //console.log("unit changed to " + unit == '0' ? 'imperial' : 'metric');

                        if (ngModel.$modelValue) {
                            if (unit == '0') { //metric to imperial
                                element.val((C2F(ngModel.$modelValue)).toFixed(1));  // change view to imperial value
                            } else { // imperial to metric
                                element.val((ngModel.$modelValue).toFixed(1)); // change view to metric value
                            }
                        }
                    });

                    if(initial_unit!=undefined) {
                        unit_scope.form.unit = initial_unit; //set to resort preferred unit
                    }
                }

                initialize();

                //scope.$watch('ngModel.$modelValue', function (value) {
                //    if (value) {
                //        console.log('model = ' + value);
                //    }
                //});
            }
        }
    }]);