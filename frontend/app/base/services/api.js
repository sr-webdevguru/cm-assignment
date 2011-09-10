angular.module('app.services')
    .service('ApiService', ['$http', '$q', '$window', '$log', 'LS', 'CONFIG', function ($http, $q, $window, $log, LS, CONFIG) {

        var service = {

            base: function () {

                var api_base = LS.get('API', '');

                if (!api_base) {
                    api_base = CONFIG.BASE_URL;
                }
                return api_base;
            },
            laravel: function(){
                var laravel_base = LS.get('LARAVEL_CORS', '');

                if (laravel_base == null || laravel_base == '') {
                    laravel_base = CONFIG.LARAVEL_URL;
                }

                return laravel_base;
            }


        };

        return service;
    }]);


