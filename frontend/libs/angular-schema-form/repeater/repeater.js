'use strict';

/**
 * repeater Module
 *
 * Description:
 *   A simple repeater directive that repeats the schema form directive.
 */
// Usage:
// $scope.model = {};
// $scope.form = [
//     {
//         "key": "employee",
//         "type": "repeater",
//         "title": "Employees",
//         "add": "Add Employee",
//         "form": [
//             "name",
//             "position"
//         ],
//         "schema": {
//             "type": "object",
//             "title": "Employee",
//             "properties": {
//                 "name": {
//                     "title": "Name",
//                     "type": "string"
//                 },
//                 "position": {
//                     "title": "Position",
//                     "type": "string"
//                 }
//             }
//         }
//     }
// ];
// $scope.schema = {
//     "type": "object",
//     "title": "",
//     "properties": {
//         "employee": {}
//     },
//     "required": []
// };

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            // Put template here as string
            var schemaTemplate =
                    '<div class="form-group">' +
                    '    <h3 ng-show="form.title && form.notitle !== true">[[form.title]]</h3>' +
                    '    <div' +
                    '        repeater="form"' +
                    '        ng-show="form.key"' +
                    '        ng-model="$$value$$">' +
                    '    </div>' +
                    '</div>',
                repeaterTemplate =
                    '<div class="schema-form-array">' +
                    '    <div class="list-group">' +
                    '        <div class="list-group-item" style="margin-bottom:10px" ' +
                    '            ng-repeat="form in repeatedForm">' +
                    '            <form' +
                    '                name="ngform"' +
                    '                name="[[repeatedFormKey]]"' +
                    '                sf-model="form.model"' +
                    '                sf-form="form.form"' +
                    '                sf-schema="form.schema"' +
                    '                ng-submit="submitForm(ngform, form.model)">' +
                    '            </form>' +
                    '            <button' +
                    '                ng-hide="form.readonly"' +
                    '                ng-click="deleteFromArray()"' +
                    '                style="position: absolute; top: 0; right: 10px; z-index: 20;"' +
                    '                type="button"' +
                    '                class="close pull-right">' +
                    '                <span aria-hidden="true">&times;</span>' +
                    '                <span class="sr-only">Close</span>' +
                    '            </button>' +
                    '            <button' +
                    '                ng-hide="readonly || add === null || [[form.title.toLowerCase() != \'injuries\']]"' +
                    '                ng-click="copyToArray([[repeatedForm.indexOf(form)]])"' +
                    '                type="button"' +
                    '                class="btn [[form.style.add || \'btn-default\']] pull-right"' +
                    '                style="position: absolute; bottom: 5px; right: 10px; z-index: 20;"' +
                    '                <i class="glyphicon glyphicon-copy"></i>' +
                    '                [[form.add || \'Copy\']]' +
                    '            </button>' +
                    '        </div>' +
                    '    </div>' +
                    '    <div class="clearfix">' +
                    '        <button' +
                    '            ng-hide="readonly || add === null"' +
                    '            ng-click="appendToArray()"' +
                    '            type="button"' +
                    '            class="btn [[form.style.add || \'btn-default\']] pull-right">' +
                    '            <i class="glyphicon glyphicon-plus"></i>' +
                    '            [[form.add || \'Add\']]' +
                    '        </button>' +
                    '    </div>' +
                    '</div>';

            // Cache template
            $templateCache.put('schema-repeater.html', schemaTemplate);
            $templateCache.put('repeater.html', repeaterTemplate);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var repeater = function (name, schema, options) {
                if (schema.type === 'repeater') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'repeater';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(repeater);

            //Add to the bootstrap directive
            schemaFormDecoratorsProvider
                .addMapping('bootstrapDecorator',
                    'repeater',
                    'schema-repeater.html');

            schemaFormDecoratorsProvider
                .createDirective('repeater',
                    'schema-repeater.html');
        }])
    .directive('repeater',
        [function () {
            // Runs during compile
            return {
                name: 'repeater',

                restrict: 'A',

                require: 'ngModel',

                scope: {
                    form: '=repeater',
                    model: '=ngModel'
                },

                templateUrl: 'repeater.html',

                replace: true,

                link: function (scope, element, attr, ngModel) {

                    //console.log(scope);
                    //console.log(element);
                    //console.log(attr);
                    //console.log(ngModel);
                    //    console.log(scope.form);
                    //    console.log(scope.model);

                    // This will update the repeater model
                    var updateModel = function () {
                        var size = scope.repeatedForm.length,
                            repeaterModel = [];
                        for (var i = 0; i < size; i++) {

                            //console.log(scope.repeatedForm);
                            //console.log(scope.repeatedForm[i]);
                            //console.log(scope.repeatedForm[i].model);

                            var model = scope.repeatedForm[i].model || {};
                            //console.log(model);
                            if (model) {
                                repeaterModel.push(model);
                            }
                        }

                        scope.model = repeaterModel;
                    };

                    // The repeater model
                    scope.repeatedForm = [];

                    //scope.$watch('ngModel.$viewValue', function (value) {
                    //    console.log(value);
                    //});

                    ngModel.$render = function () {
                        var value = ngModel.$viewValue;
//                    console.log("render");
//                    console.log(value);

                        if (value && value.length > 0) {
                            var size = value.length,
                                forms = [];
                            for (var i = 0; i < size; i++) {
                                var form = angular.copy(scope.form);
                                form.model = value[i];

                                forms.push(form);
                            }

                            scope.repeatedForm = forms;

//                        once();
                        }
                    };

                    // Watch for form changes
//                scope.$watch('repeatedForm', function (value) {
//                    updateModel();
//                }, true);

//                var once = scope.$watch('model', function (value) {
//                    console.log("model got updated");
//                    console.log(value);
//
//                    if (value && value.length > 0) {
//                        var size = value.length,
//                            forms = [];
//                        for (var i = 0; i < size; i++) {
//                            var form = angular.copy(scope.form);
//                            form.model = value[i];
//
//                            forms.push(form);
//                        }
//
//                        scope.repeatedForm = forms;
//
//                        once();
//                    }
//                });

                    // Deletes a repeated form from array
                    scope.deleteFromArray = function () {
                        var index = this.$index;
                        if (index !== undefined) {
                            scope.repeatedForm.splice(index, 1);
                            updateModel();
                        }
                    };

                    // Adds a schema form with empty properties
                    scope.appendToArray = function () {
                        var form = angular.copy(scope.form);
                        scope.repeatedForm.push(form);
                        updateModel();
                    };

                    scope.copyToArray = function (id) {
                        if(scope.repeatedForm.length > 0) {
                            scope.repeatedForm.push(angular.copy(scope.repeatedForm[id]));
                        }
                        else {
                            var form = angular.copy(scope.form);
                            scope.repeatedForm.push(form);
                        }
                        updateModel();
                    };
                }
            };
        }]);