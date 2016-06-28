angular.module('app').factory('langLoader', function ($http, $q, ApiService, CONFIG, LS) {
    return function (options) {
        var deferred = $q.defer();

        var data = LS.get(options.key, false);

        if (data) {
            data = JSON.parse(data);
            LS.set(options.key, JSON.stringify(data));

            deferred.resolve(data);
        } else {
            $http.get(ApiService.base() + CONFIG.API_URL + '/language/', {
                params: {
                    lang: options.key
                }
            })
                .success(function (data) {
                    LS.set(options.key, JSON.stringify(data));

                    deferred.resolve(data);
                }).error(function () {
                    deferred.reject(options.key);
                });
        }


        return deferred.promise;
    }
});