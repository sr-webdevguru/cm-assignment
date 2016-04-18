'use strict';

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            var schemaHtml =
                '<div class="form-inline" style="margin-bottom:15px;">' +
                '<div class="form-group" ng-class="{\'has-error\': hasError(), \'has-success\': hasSuccess(), \'has-feedback\': form.feedback !== false}" ng-show="form.key">' +
                '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                '   <div>' +
                '       <input type="number" class="form-control" name="[[ form.key.slice(-1)[0] ]]" min="[[ form.min ]]" max="[[ form.max ]]" weight schema-validate="form" ng-model="$$value$$" ng-pattern="/^(\\-)?[0-9]{1,3}(\\.[0-9]+)?$/">' +
                '   </div>' +
                '</div>' +
                '<div  class="form-group" style="margin:15px 0 0 15px;">' +
                '   <label class="control-label"></label>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_weight" value="0" ng-model="form.unit"> lbs</label>' +
                '   </div>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_weight" value="1" ng-model="form.unit"> kg</label>' +
                '   </div>' +
                '   </div>' +
                '</div>';
            '</div>';

            $templateCache.put('weight.html', schemaHtml);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var weight = function (name, schema, options) {
                if (schema.type === 'weight') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'weight';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(weight);

            schemaFormDecoratorsProvider.addMapping(
                'bootstrapDecorator',
                'weight',
                'weight.html'
            );

            schemaFormDecoratorsProvider.createDirective(
                'weight',
                'weight.html'
            );
        }])
    .directive('weight',
    ['$http', '$parse', function ($http, $parse) {
        return {
            restrict: 'A',
            require: 'ngModel',

            link: function (scope, element, attrs, ngModel) {
                function lbs2kg(value) {
                    return (value / 2.2046);
                }

                function kg2lbs(value) {
                    return (value * 2.2046);
                }


                function initialize() {
                    var unit_scope = angular.element(element.parent().parent().parent().find("input[type=radio]").get(0)).scope();
                    var initial_unit = unit_scope.form.unit;

                    // => view -> model => model always keep "metric" value
                    ngModel.$parsers.push(function (viewValue) {
                        var modelValue = parseFloat(viewValue); //set to defined unit
                        if (unit_scope.form.unit == '0') { //imperial
                            return parseFloat((lbs2kg(modelValue)).toFixed(0));
                        } else {
                            return parseFloat((modelValue).toFixed(0));
                        }
                    });

                    unit_scope.form.unit = '1'; // set to metric (saved unit)
                    // now model and view values are same

                    //set up watch
                    unit_scope.$watch('form.unit', function (unit) {
                        //console.log("unit changed to " + unit == '0' ? 'imperial' : 'metric');

                        if (ngModel.$modelValue) {
                            if (unit == '0') { //metric to imperial
                                element.val((kg2lbs(ngModel.$modelValue)).toFixed(0));  // change view to imperial value
                            } else { // imperial to metric
                                element.val((ngModel.$modelValue).toFixed(0)); // change view to metric value
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