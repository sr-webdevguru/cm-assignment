'use strict';

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            var schemaHtml =
                '<div class="form-group" ng-class="{\'has-success\': hasSuccess}"' +
                '   ng-show="form.key">' +
                '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                '<div class="row">' +
                '<div class="col-lg-3 col-md-4 col-xs-6" ng-repeat="item in form.choices">' +
                '<label>' +
                '<input type="checkbox" checklist-model="$$value$$" name="[[ form.key.slice(-1)[0] ]]" checklist-value="item.id">' +
                ' [[item.name]]' +
                '</label>' +
                '</div>' +
                '</div>' +
//            '   <select' +
//            '       ng-change="onSelectChange()"' +
//            '       multiple sf-changed="form" ' +
//            '       ng-model="$$value$$" name="[[ form.key.slice(-1)[0] ]]"' +
//            '       class="form-control" ng-options=\"item.id as item.name for item in form.choices\">' +
//            '       <option' +
//            '           value="[[option.id]]"' +
//            '           ng-repeat="option in form.choices">' +
//            '           [[option.name]]' +
//            '       </option>' +
//            '   </select>' +
//            '<p style="font-size: 12px; padding-top:4px;">Hold Ctrl on your keyboard and click to select multiple values</p>'+
                '</div>';

            $templateCache.put('multiselect.html', schemaHtml);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var multiselect = function (name, schema, options) {
                if (schema.type === 'multiselect') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'multiselect';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(multiselect);

            schemaFormDecoratorsProvider.addMapping(
                'bootstrapDecorator',
                'multiselect',
                'multiselect.html'
            );

            schemaFormDecoratorsProvider.createDirective(
                'multiselect',
                'multiselect.html'
            );
        }])