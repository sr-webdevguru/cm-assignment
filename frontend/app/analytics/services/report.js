angular.module('app.services')
    .service('ReportService', ['$http', '$q', '$log', 'UserService', 'LS',  'CONFIG', 'ApiService', function ($http, $q, $log, UserService, LS, CONFIG, ApiService) {

        var API = {
            base:  CONFIG.API_URL + '/reports/',
            getUrl: function (id) {
                return '/' + id;
            }
        };

        return {
            fetchAll: function (dateFrom, dateTo, resort_id, chunk, page) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base)
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

                $http.get(ApiService.base() + API.base + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchPatrollers: function (params) {
                var d = $q.defer();
                var query = [];
                for(var key in params){
                    if (params.hasOwnProperty(key))
                        query.push(key + '=' + params[key]);
                }
                $http.get(ApiService.base() + API.base + 'patrollers/?' + query.join('&'))
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            create: function (data) {
                var params = data || {};

                var d = $q.defer();

                $http.post(ApiService.base() + API.base, params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            update: function (id, data) {

                var params = data || {};

                var d = $q.defer();

                $http.put(ApiService.base() + API.base + id + '/', params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            }
        };
    }]);


