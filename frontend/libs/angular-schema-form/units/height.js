'use strict';

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            var schemaHtml =
                '<div class="form-inline" style="margin-bottom:15px;">' +
                '<div class="form-group" ng-class="{\'has-error\': hasError(), \'has-success\': hasSuccess(), \'has-feedback\': form.feedback !== false}" ng-show="form.key">' +
                '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                '   <div>' +
                '       <input type="number" class="form-control" name="[[ form.key.slice(-1)[0] ]]" min="[[ form.min ]]" max="[[ form.max ]]" heightsf schema-validate="form" ng-model="$$value$$" ng-pattern="/^(\\-)?[0-9]{1,3}(\\.[0-9]+)?$/" style="max-width: 80px;"><span ng-hide="form.unit==1"> ft</span>' +
                '       <input type="number" class="form-control secondary" name="[[ form.key.slice(-1)[0] ]]_secondary" min="0" max="11.9" ng-model="inches" ng-pattern="/^(\\-)?[0-9]{1}(\\.[0-9]+)?$/" style="max-width: 80px;" ng-hide="form.unit==1"><span ng-hide="form.unit==1"> in</span>' +
                '   </div>' +
                '</div>' +
                '<div  class="form-group" style="margin:15px 0 0 15px;">' +
                '   <label class="control-label"></label>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_heightsf" value="0" ng-model="form.unit"> ft</label>' +
                '   </div>' +
                '   <div class="radio">' +
                '       <label><input type="radio" name="[[ form.key.slice(-1)[0] ]]_heightsf" value="1" ng-model="form.unit"> cm</label>' +
                '   </div>' +
                '   </div>' +
                '</div>';
            '</div>';

            $templateCache.put('heightsf.html', schemaHtml);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var heightsf = function (name, schema, options) {
                if (schema.type === 'heightsf') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'heightsf';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(heightsf);

            schemaFormDecoratorsProvider.addMapping(
                'bootstrapDecorator',
                'heightsf',
                'heightsf.html'
            );

            schemaFormDecoratorsProvider.createDirective(
                'heightsf',
                'heightsf.html'
            );
        }])
    .directive('heightsf',
    ['$http', '$parse', '$timeout', function ($http, $parse, $timeout) {
        return {
            restrict: 'A',
            require: 'ngModel',

            link: function (scope, element, attrs, ngModel) {
                function ft2cm(ft, inches) {
                    return (ft * 12 + inches) * 2.54;
                }

                function cm2ft(value) {
                    return {
                        ft: Math.floor(value * 0.39370078740157 / 12),
                        inches: (value * 0.39370078740157) % 12
                    };
                }

                function update_inches(value) {
                    //console.log("update inches: " + value);
                    if (value) {
                        var inches = parseFloat(value).toFixed(0);

                        $timeout(function () {
                            var elem_inches = angular.element(element.parent().find("input.secondary").get(0));
                            elem_inches.val(inches);
                        }, 10);
                    }
                }


                function initialize() {
                    var unit_scope = angular.element(element.parent().parent().parent().find("input[type=radio]").get(0)).scope();
                    var elem_inches = angular.element(element.parent().find("input.secondary").get(0));
                    var inches_scope = elem_inches.scope();

                    var initial_unit = unit_scope.form.unit;
                    unit_scope.form.unit = '1'; // set to metric (saved unit)
                    // now model and view values are same

                    // => view -> model => model always keep "metric" value
                    ngModel.$parsers.push(function (viewValue) {
                        if (viewValue) {
                            //console.log("parser: " + viewValue);
                            if (unit_scope.form.unit == '0') { //imperial
                                var inches = parseFloat(elem_inches.val()) || 0;
                                //console.log("parser imperial: " + viewValue + "    " + inches);
                                return parseFloat((ft2cm(viewValue, inches)).toFixed(0));
                            } else {
                                //console.log("parser metric: " + viewValue);
                                return parseFloat((viewValue).toFixed(0));
                            }
                        }
                    });

                    inches_scope.$watch('inches', function (newValue, oldValue) {
                        //console.log("inches watch: " + newValue + "    " + oldValue  );
                        if(newValue && newValue!==oldValue) {
                            if (unit_scope.form.unit == '0') {
                                //var inches = value||0;
                                var ft = parseFloat(element.val()) || 0;
                                update_inches(newValue);
                                ngModel.$setViewValue(ft);
                            }
                        }else{

                        }
                    });

                    unit_scope.$watch('form.unit', function (unit, old_unit) {
                        //console.log("unit watch: " + unit);
                        if (ngModel.$modelValue && unit !== old_unit) {

                            if (unit == '0') { //metric to imperial
                                var value = cm2ft(ngModel.$modelValue);

                                element.val((value.ft).toFixed(0));  // change view to imperial value
                                update_inches(value.inches);
                            } else { // imperial to metric
                                element.val((ngModel.$modelValue).toFixed(0)); // change view to metric value
                            }
                        }
                    });

                    $timeout(function () {
                        if (initial_unit !== '1') {
                            unit_scope.form.unit = initial_unit; //set to resort preferred unit
                        }
                    }, 10);
                }

                initialize();

                //scope.$watch('ngModel.$modelValue', function (value) {
                //    console.log('model = ' + value);
                //});
            }
        }
    }]);