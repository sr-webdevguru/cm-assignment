angular.module('app.services')
    .service('LocationService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {
            fetchAll: function (chunk, page, text, areaId, predicate, direction) {
                var d = $q.defer();

                predicate = predicate || 'location_name';
                direction = direction || false;

                $http.get(ApiService.base() + CONFIG.API_URL + '/locations/',
                    {
                        params: {
                            chunk: chunk,
                            offset: (page - 1) * chunk,
                            search: text,
                            area_id: areaId,
                            order_by: predicate,
                            order_by_direction: direction ? 'desc' : 'asc'
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

            update: function (id, name, area_id, map_lat, map_long) {
                var d = $q.defer();

                var params = {
                    'location_name': name,
                    'area_id': area_id,
                    'map_lat': map_lat,
                    'map_long': map_long
                };

                $http.put(ApiService.base() + CONFIG.API_URL + '/locations/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            add: function (name, area_id, map_lat, map_long) {
                var d = $q.defer();
                var params = {
                    'location_name': name,
                    'area_id': area_id,
                    'map_lat': map_lat,
                    'map_long': map_long
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/locations/', params)
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

                $http.get(ApiService.base() + CONFIG.API_URL + '/locations/' + id + '/')
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
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                };

                $http.delete(ApiService.base() + CONFIG.API_URL + '/locations/' + id + '/', params)
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


