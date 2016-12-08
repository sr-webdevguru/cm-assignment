angular.module('app.services')
    .service('ResortService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {
//            saveUser: function (id, name, email, role, phone, asset_mgmt, controlled_subs) {
//                var d = $q.defer();
//
//                var params = {
//                    'name': name,
//                    'email': email,
//                    'role_id': role,
//                    'phone': phone,
//                    'user_asset_management':asset_mgmt,
//                    'user_controlled_substances':controlled_subs
//                };
//
//                $http.put(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/', params)
//                    .success(function (response, status, headers) {
//                        d.resolve(response.data);
//                    })
//                    .error(function (response, status, headers, config, errors) {
//                        d.reject(response);
//                    });
//
//                return d.promise;
//            },
//
//            addUser: function (name, email, phone, role) {
//                var d = $q.defer();
//                var resort_id = JSON.parse(LS.get('user')).resorts[0].resort_id;
//                var params = {
//                    'name': name,
//                    'email': email,
//                    'phone': phone,
//                    'role_id': parseInt(role),
//                    'password': "T3mP4$$0143",
//                    'resort_id': resort_id
//                };
//
//                $http.post(ApiService.base() + CONFIG.API_URL + '/users/', params)
//                    .success(function (response, status, headers) {
//                        d.resolve(response.data);
//                    })
//                    .error(function (response, status, headers, config, errors) {
//                        d.reject(response);
//                    });
//
//                return d.promise;
//            },
            fetchAll: function (chunk, page, text, predicate, direction) {
                var d = $q.defer();

                predicate = predicate || 'name';
                direction = direction || false;

                $http.get(ApiService.base() + CONFIG.API_URL + '/users/',
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

                $http.get(ApiService.base() + CONFIG.API_URL + '/resorts/' + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            removeUser: function (id, first_name, last_name, email) {
                var d = $q.defer();

                var params = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                };

                $http.delete(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchSettings: function (id) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/resorts/' + id + '/settings/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            updateSettings: function (id, data) {
                var d = $q.defer();

                $http.put(ApiService.base() + CONFIG.API_URL + '/resorts/' + id + '/settings/', data)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            generateOAuth: function (id, data) {
                var d = $q.defer();

                $http.post(ApiService.base() + CONFIG.API_URL + '/resort_oauth/?operation=generate', data)
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            regenerateOAuth: function (id, data) {
                var d = $q.defer();

                $http.post(ApiService.base() + CONFIG.API_URL + '/resort_oauth/?operation=regenerate', data)
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },
        };

        return service;
    }]);


