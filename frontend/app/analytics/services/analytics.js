angular.module('app.services')
    .service('AnalyticsService', ['$http', '$q', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $log, LS, CONFIG, ApiService) {


        var API = {
            base: CONFIG.API_URL + '/analytics',
            getUrl: function (id) {
                return '/' + id;
            }
        };

        var REPORT_API = {
            base: CONFIG.API_URL + '/reports'
        };


        var service = {
            fetchSex: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/gender', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchActivity: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/activity', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchInjury: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/injury_types', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchReferred: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/referred_to', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchAge: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/age', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchAlcohol: function (dateFrom, dateTo, resort_id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + '/alcohol', {
                    params: {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchPatrollers: function (dateFrom, dateTo) {
                var d = $q.defer();

                $http.get(ApiService.base() + REPORT_API.base + '/patrollers/', {
                    params: {
                        output_format: 'json',
                        datefrom: dateFrom,
                        dateto: dateTo,
                        offset: 0,
                        chunk: 20,
                        order_by: "name",
                        order_by_direction: "asc"
                    }
                })
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            }


        };

        return service;
    }]);
