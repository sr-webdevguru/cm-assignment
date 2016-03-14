angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            $templateCache
                .put('directives/decorators/bootstrap/imagemodal/imagemodal.html',
                    '<div class="form-group">' +
                    '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                    '    <div' +
                    //'        name="[[form.key]]"' +
                    '        ng-show="form.key"' +
                    '        class="form-control"' +
                    '        schema-validate="form" image-modal' +
                    '        ng-model="$$value$$"' +
                    '        image-is-zoomable="form.enableZoom"' +
                    '        image-is-uploadable="form.enableUpload"' +
                    '        image-is-removable="form.enableRemove"></div>' +
                    '</div>');
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var imagemodal = function (name, schema, options) {
                if (schema.type === 'image' && schema.format === 'string') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'image';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(imagemodal);

            //Add to the bootstrap directive
            schemaFormDecoratorsProvider
                .addMapping('bootstrapDecorator',
                'image',
                'directives/decorators/bootstrap/imagemodal/imagemodal.html');
            schemaFormDecoratorsProvider
                .createDirective('imagemodal',
                'directives/decorators/bootstrap/imagemodal/imagemodal.html');
        }]);