angular.module('app.services')
    .service('AssetService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {
            fetchAll: function (chunk, page, text, predicate, direction) {
                var d = $q.defer();

                predicate = predicate || 'asset_name';
                direction = direction || false;

                $http.get(ApiService.base() + CONFIG.API_URL + '/assets/',
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

            update: function (id, name, asset_type_id, location_id) {
                var d = $q.defer();

                var params = {
                    'asset_name': name,
                    'asset_type_id': asset_type_id,
                    'location_id': location_id
                };

                $http.put(ApiService.base() + CONFIG.API_URL + '/assets/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            add: function (name, asset_type_id, area_id, location_id) {
                var d = $q.defer();
                var params = {
                    'asset_name': name,
                    'asset_type_id': asset_type_id,
                    'location_id': location_id
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/assets/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },


            fetch: function (id) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/assets/' + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            remove: function (id, first_name, last_name, email) {
                var d = $q.defer();

                var params = {
                };

                $http.delete(ApiService.base() + CONFIG.API_URL + '/assets/' + id + '/', params)
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


