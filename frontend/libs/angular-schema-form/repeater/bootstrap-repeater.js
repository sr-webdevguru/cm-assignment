angular.module('schemaForm')
.run(['$templateCache',
      function($templateCache) {
    // Put template here as string
    var template =
        '<div class="form-group">' +
        '    <label class="control-label" ng-show="form.title && form.notitle !== true">{{ form.title }}</label>' +
        '    <div' +
        '        repeater="form"' +
        '        ng-show="form.key"' +
        '        ng-model="$$value$$">' +
        '    </div>' +
        '</div>';

    // Cache template
    $templateCache.put('repeater/schema-repeater.html', template);
}])
.config(['schemaFormProvider',
         'schemaFormDecoratorsProvider',
         'sfPathProvider',
         function(schemaFormProvider,
                  schemaFormDecoratorsProvider,
                  sfPathProvider) {

    var repeater = function(name, schema, options) {
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
                    'repeater/schema-repeater.html');

    schemaFormDecoratorsProvider
        .createDirective('repeater',
                         'repeater/schema-repeater.html');
}]);