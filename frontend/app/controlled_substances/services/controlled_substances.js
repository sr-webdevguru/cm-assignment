angular.module('app.services')
    .service('ControlledSubstanceService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {
            fetchAll: function (chunk, page, text, predicate, direction) {
                var d = $q.defer();

                predicate = predicate || 'controlled_substance_name';
                direction = direction || false;

                $http.get(ApiService.base() + CONFIG.API_URL + '/controlled_substances/',
                    {
                        params: {
                            chunk: chunk,
                            offset: (page - 1) * chunk,
                            search:text,
                            order_by:predicate,
                            order_by_direction: direction?'desc':'asc'
                        }
                    })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetch: function (id) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/controlled_substances/' + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            add: function (name, units) {
                var d = $q.defer();
                var params = {
                    'controlled_substance_name': name,
                    'units': units
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            update: function (id, name, units) {
                var d = $q.defer();

                var params = {
                    'controlled_substance_name': name,
                    'units': units
                };

                $http.put(ApiService.base() + CONFIG.API_URL + '/controlled_substances/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            remove: function (id) {
                var d = $q.defer();

                var params = {
                };

                $http.delete(ApiService.base() + CONFIG.API_URL + '/controlled_substances/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            }
        };

        return service;
    }]);


