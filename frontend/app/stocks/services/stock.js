angular.module('app.services')
    .service('StockService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {
            fetchAll: function (chunk, page, text, predicate, direction, current_status, location_id, controlled_substance_id, dateFrom, dateTo ) {
                var d = $q.defer();

                predicate = predicate || 'controlled_substance__controlled_substance_name';
                direction = direction || false;

                if(location_id=='__empty__'){
                    location_id='';
                }

                $http.get(ApiService.base() + CONFIG.API_URL + '/controlled_substances/report/',
                    {
                        params: {
                            date_from: dateFrom,
                            date_to: dateTo,
                            chunk: chunk,
                            offset: (page - 1) * chunk,
                            current_status:current_status,
                            order_by:predicate,
                            order_by_direction: direction?'desc':'asc',
                            location_id:location_id,
                            controlled_substance_id:controlled_substance_id
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

            add: function (quantity, controlled_substance_id, volume,location_id, dt_expiry) {
                var d = $q.defer();
                var params = {
                    'quantity': quantity,
                    'controlled_substance_id': controlled_substance_id,
                    'volume': volume,
                    'location_id': location_id,
                    'dt_expiry': dt_expiry
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/add/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            checkout: function (controlled_substance_stock_id, user_id) {
                var d = $q.defer();
                var params = {
                    'controlled_substance_stock_id': controlled_substance_stock_id,
                    'user_id': user_id
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/checkout/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            checkin: function (controlled_substance_stock_assignment_id, location_id) {
                var d = $q.defer();
                var params = {
                    'controlled_substance_stock_assignment_id': controlled_substance_stock_assignment_id,
                    'location_id':location_id
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/checkin/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            relocate: function (controlled_substance_stock_id, location_id) {
                var d = $q.defer();
                var params = {
                    'controlled_substance_stock_id': controlled_substance_stock_id,
                    'location_id': location_id
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/relocate/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            dispose: function (controlled_substance_stock_id) {
                var d = $q.defer();
                var params = {
                    'controlled_substance_stock_id': controlled_substance_stock_id,
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/controlled_substances/dispose/', params)
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


