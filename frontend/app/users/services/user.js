angular.module('app.services')
    .service('UserService', ['$http', '$q', '$window', '$intercom', '$log', 'LS', 'CONFIG', 'ApiService', function ($http, $q, $window, $intercom, $log, LS, CONFIG, ApiService) {

        var service = {

            user: null,
            is_authenticated: false,

            discover: function (email) {

                var data = {
                    'email': email || ''
                };

                var d = $q.defer();

                $http.post(ApiService.base() + CONFIG.API_URL + '/auth/discover/', data)
                    .success(function (data, status, headers) {

                        var mapping = {
                            'app.medic52.local': CONFIG.BASE_URL,
                            'app-dev.medic52.com': data.location,
                            'app-dev-us.medic52.com': data.location,
                            'app-dev-au.medic52.com': data.location,
                            'app-staging.medic52.com': data.location,
                            'app.medic52.com': data.location,
                            'localhost:8095': 'http://localhost:8090'
                        };
                        var laravelMapping = {
                            'app.medic52.local': CONFIG.LARAVEL_URL,
                            'app-dev.medic52.com': data.laravel_location,
                            'app-dev-us.medic52.com': data.laravel_location,
                            'app-dev-au.medic52.com': data.laravel_location,
                            'app-staging.medic52.com': data.laravel_location,
                            'app.medic52.com': data.laravel_location,
                            'localhost:8095': 'http://localhost:8100'
                        };

                        var host = window.location.host;
                        LS.set('API', mapping[host]);
                        LS.set('LARAVEL_CORS', laravelMapping[host]);

                        console.log(laravelMapping);
                        console.log(host);
                        console.log(laravelMapping[host]);
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        $log.log(data);

                        LS.set('API', '');

                        d.reject(data);
                    });

                return d.promise;
            },

            login: function (email, password) {

                var data = {
                    'email': email || '',
                    'password': password || ''
                };

                var d = $q.defer();

                $http.post(ApiService.base() + CONFIG.API_URL + '/auth/login/', data)
                    .success(function (data, status, headers) {
                        var rolesArr = ['', 'Patroller', 'Dispatcher', 'Manager'];

                        data.user.role = rolesArr[data.user.role_id[0].value];

                        data.user.role_id.forEach(function (entry) {
                            if (entry.value == 3) {
                                data.user.isManager = true;
                            }
                        });
                        service.user = data.user;
                        service.user.role = data.user.role;
                        service.is_authenticated = true;

                        LS.set('user', JSON.stringify(service.user));
                        LS.set('token', 'Token ' + data.user.token);

                        $intercom.update({
                            email: service.user.email,
                            name: service.user.name,
                            created_at: new Date(),
                            user_id: service.user.user_id,
                            company: {
                                id: service.user.resorts[0].resort_id,
                                name: service.user.resorts[0].resort_name
                            },
                            role: service.user.role_id[0].key,
                            dashboard_feature_last_used: "Login",
                            user_connected: service.user.user_connected.value
                        });


                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {

                        $log.log(data);

                        service.user = null;
                        service.is_authenticated = false;

                        LS.set('user', null);

                        d.reject(data);
                    });

                return d.promise;
            },


            logout: function () {
                if (service.user && service.user.hasOwnProperty('user_id') && service.user.user_id) {

                    var d = $q.defer();

                    var data = {};

                    $http.post(ApiService.base() + CONFIG.API_URL + '/auth/logout/' + service.user.user_id + '/', data)
                        .success(function (data, status, headers) {

                            service.user = null;
                            service.is_authenticated = false;
                            LS.set('user', null);
                            LS.set('token', null);
                            LS.set('API', '');
                            LS.set('en_US', '');

                            d.resolve(data);

                        })
                        .error(function (data, status, headers, config, errors) {
                            d.reject(data);
                        });

                    return d.promise;
                }
            },

            currentUser: function () {
                return service.user;
//                var d = $q.defer();
//                $http.get(CONFIG.API_BASE_URL + '/auth/current_user')
//                    .success(function (response, status, headers) {
//                        d.resolve(response.data);
//                    })
//                    .error(function (data, status, headers, config, errors) {
//                        d.reject(data);
//                    });
//
//                return d.promise;
            },

            currentRole: function () {
                return service.user.role;
            },

            saveUser: function (id, name, email, role, phone, asset_mgmt, controlled_subs) {
                var d = $q.defer();

                var params = {
                    'name': name,
                    'email': email,
                    'role_id': role,
                    'phone': phone,
                    'user_asset_management':asset_mgmt,
                    'user_controlled_substances':controlled_subs
                };

                $http.put(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            addUser: function (name, email, phone, role) {
                var d = $q.defer();
                var resort_id = JSON.parse(LS.get('user')).resorts[0].resort_id;
                var params = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'role_id': parseInt(role),
                    'password': "T3mP4$$0143",
                    'resort_id': resort_id
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/users/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },
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

                $http.get(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchDevices: function (id) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/devices/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            forgotPassword: function (email) {
                var d = $q.defer();

                var params = {
                    'email': email
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/auth/password_reset/', params)
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            resetPassword: function (id, first_name, last_name, email) {
                var d = $q.defer();

                var params = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                };

                $http.post(ApiService.base() + CONFIG.API_URL + '/users/' + id + '/resetpassword', params)
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

            updateUserStatus: function (user_id, resort_id, type) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/users/' + user_id + '/status/',
                    {
                        params : {
                            type: type,
                            resort_id: resort_id
                        }
                    }
                )
                .success(function (response, status, headers) {
                    d.resolve(response.detail);
                })
                .error(function (response, status, headers, config, errors) {
                    d.reject(response);
                });

                return d.promise;
            },

            testDevice: function (deviceId) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/devices/' + deviceId + '/test_notifications/')
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            removeDevice: function (deviceId) {
                var d = $q.defer();

                $http.put(ApiService.base() + CONFIG.API_URL + '/devices/' + deviceId + '/', {'device_state': 2})
                    .success(function (response, status, headers) {
                        d.resolve(response.data);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            }
        };

        function init() {
            if (LS.get('user') == null || LS.get('user') == "null" || LS.get('user') == "" || LS.get('user') == undefined) {
                LS.set('user', null);
            } else {
                service.user = JSON.parse(LS.get('user'));
                service.is_authenticated = true;
            }
        }

        init();

        return service;
    }]);


