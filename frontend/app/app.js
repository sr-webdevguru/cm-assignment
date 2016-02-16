'use strict';

angular.module('app', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ui.router',
    'ui.bootstrap',
    'mgcrea.ngStrap',
    'angular-loading-bar',
    'checklist-model',
    'ngIdle',
    'ngCsv',
    'pascalprecht.translate',
    'googlechart',
    'angular-growl',
    "leaflet-directive",
    'cfp.hotkeys',
    'schemaForm',
    'schemaForm-file-upload',
    //'restangular',
    'ngIntercom',
    'ui.bootstrap.datetimepicker',
    'number-input',

    'app.services'
])
    .constant('OAUTH', {
        CLIENT_ID: 'ZnojInHgal74Jx36phDURgtLWBBONF5JXBa2hWG4',
        CLIENT_SECRET: 'GxZ05xIV5bzAc99vO5lIscfUmsKIvv5TDzeZc9VpijncAHn2Car8nOSGdYENLwje278EsgQtC3YVvgReRCSMbId8BhwUM2j66ps3rlUUXNmDDfeyOfwygIBpHjZVIwah'
    })
    .factory('CONFIG', function ($location) {
        var mapping = {
            'app.medic52.local': 'api.medic52.local',
            'app-dev.medic52.com': 'api-dev-us.medic52.com',
            'app-dev-us.medic52.com': 'api-dev-us.medic52.com',
            'app-staging.medic52.com': 'api-staging-us.medic52.com',
            'app.medic52.com': 'api-us.medic52.com',
            'localhost': 'localhost:8090'
        };
        var laravelMapping = {
            'api.medic52.local': 'api.medic52.local',
            'api-dev.medic52.com': 'api-dev-us.medic52.com',
            'api-dev-us.medic52.com': 'api-dev-us.medic52.com',
            'api-staging.medic52.com': 'api-staging-us.medic52.com',
            'api.medic52.com': 'api-us.medic52.com',
            'localhost': 'localhost:8090'
        };

        var host = $location.host();
//        var subdomain = host.split('.')[0];
//        host = host.replace(subdomain, mapping[subdomain]);

        return {
            BASE_URL: $location.protocol() + "://" + mapping[host], //        BASE_URL: 'https://api-dev-us.medic52.com',
            API_URL: '/api/v3',
            LARAVEL_URL: $location.protocol() + "://" + laravelMapping[host]
        }
    })
//    .factory('INTERCOM_APPID', function ($location) {
//        var mapping = {
//            'app.medic52.local': 'y5rk20en',
//            'app-dev.medic52.com': 'y5rk20en',
//            'app-staging.medic52.com': 'y5rk20en',
//            'app.medic52.com': 'cxj57moj'
//
//        };
//
//        var host = $location.host();
//        return mapping[host];
//    })
    .factory('authHttpResponseInterceptor', function ($q, $location, $log, $injector) {
        return {
            request: function (config) {
                var LS = $injector.get('LS');
                var ApiService = $injector.get('ApiService');
                var authorization = LS.get('Authorization');
                var token = LS.get('token');
                
                var getURL = config.url;
                if (getURL.includes('s3.amazonaws.com')){
                    console.log('S3 call no auth header required');
                }else{
                    if (authorization != null) {
                        config.headers['Authorization'] = authorization;
                    }

                    if (token != null) {
                        config.headers['token'] = token;
                    }
                }

                return config;
            },
            responseError: function (rejection) {

                var ApiService = $injector.get('ApiService');

                if (rejection.status === 401) {

                    if (rejection.hasOwnProperty('data') && rejection.data.hasOwnProperty('detail') && (rejection.data.detail.indexOf("token_has_expired") != -1 || rejection.data.detail.indexOf("no_access_token_provided") != -1)) {
                        $log.log("Refresh Token ", rejection);

                        var LS = $injector.get('LS');
                        var $http = $injector.get('$http');
                        var OAUTH = $injector.get('OAUTH');

                        var deferred = $q.defer();

                        var auth = {
                            'grant_type': 'client_credentials',
                            'client_id': OAUTH.CLIENT_ID,
                            'client_secret': OAUTH.CLIENT_SECRET
                        };

                        //recover token and create a new session
                        $http({
                            method: 'POST',
                            url: ApiService.base() + '/oauth/access_token/',
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            transformRequest: function (obj) {
                                var str = [];
                                for (var p in obj)
                                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                                return str.join("&");
                            },
                            data: auth
                        })
                            .success(function (data, status, headers) {
                                LS.set('Authorization', data.token_type + ' ' + data.access_token);
                                rejection.config.headers['Authorization'] = data.token_type + ' ' + data.access_token;
                                deferred.resolve(data);
                            })
                            .error(function (data, status, headers, config, errors) {
                                deferred.reject(data);
                            });


                        // When the session recovered, make the same backend call again and chain the request
                        return deferred.promise.then(function () {
                            return $http(rejection.config);
                        });

                    } else {
                        $log.log("401: ", rejection.data.detail);
                        $location.path('/login')
                    }

                }
                return $q.reject(rejection);
            }
        }
    })
    .config(function ($intercomProvider) {
        var mapping = {
            'app.medic52.local': 'y5rk20en',
            'app-dev.medic52.com': 'y5rk20en',
            'app-staging.medic52.com': 'y5rk20en',
            'app.medic52.com': 'cxj57moj',
            'localhost:8095': 'y5rk20en'
        };

        var host = window.location.host;
        var INTERCOM_APPID = mapping[host];


        // Either include your app_id here or later on boot
        $intercomProvider.appID(INTERCOM_APPID);

        // you can include the Intercom's script yourself or use the built in async loading feature
        $intercomProvider.asyncLoading(true);
    })
    .config(function (IdleProvider, KeepaliveProvider) {

        // configure IdleProvider settings
        IdleProvider.idle(1800); // in seconds
        IdleProvider.timeout(120); // in seconds

//            KeepaliveProvider.interval(2); // in seconds
    })
    .config(['growlProvider', function (growlProvider) {
        growlProvider.globalTimeToLive({success: 4000, error: 6000, warning: 6000, info: 4000});
        growlProvider.globalPosition('top-center');
        growlProvider.globalDisableCountDown(true);
    }])
    .config(function ($httpProvider) {
        $httpProvider.interceptors.push('authHttpResponseInterceptor');

        //RestangularProvider.setBaseUrl("/api/v3");

        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        if (!$httpProvider.defaults.headers.get) {
            $httpProvider.defaults.headers.get = {};
        }
        //disable IE ajax request caching
        //$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
    })
    .config(function ($interpolateProvider, $compileProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        $compileProvider.imgSrcSanitizationWhitelist(/^\s*(http|https|blob|data):/);
    })
    .config(function ($translateProvider) {
        $translateProvider.useLoader('langLoader', {});
        $translateProvider.preferredLanguage('en_US');
    })
    .config(function ($stateProvider, $urlRouterProvider, $locationProvider) {

        var currentUser = function (UserService) {
            return UserService.currentUser();
        };

        var questions = function (QuestionService) {
            return QuestionService.fetch();
        };

        var assetTypes = function (AssetTypeService) {
            return AssetTypeService.fetchAll();
        };

        var areas = function (AreaService) {
            return AreaService.fetchAll(10000, 1);
        };

        var locations = function (LocationService) {
            return LocationService.fetchAll(10000, 1);
        };

        var controlledSubstances = function (ControlledSubstanceService) {
            return ControlledSubstanceService.fetchAll(10000, 1);
        };

        var incidentStatus = function(IncidentService){
            return IncidentService.getStatuses();
        };

        // TODO : Handle this when multiple resort scenario is handled
        var resortSettings = function(ResortService, currentUser) {
            return ResortService.fetchSettings(currentUser.resorts[0].resort_id);
        };

//        // Global router
        $urlRouterProvider
            .otherwise('/map');

        // Without # in URL
        //$locationProvider.html5Mode(true);

        // Views
        var login = {
            templateUrl: '/app/auth/templates/login.html',
            controller: 'AuthCtrl'
        };

        var password_forgot = {
            templateUrl: '/app/auth/templates/password/forgot.html',
            controller: 'AuthCtrl',
            resolve: {currentUser: currentUser}
        };


        var password_reset = {
            templateUrl: '/app/auth/templates/password/reset.html',
            controller: 'AuthCtrl',
            resolve: {currentUser: currentUser}
        };

        var header = {
            templateUrl: '/app/base/templates/header.html',
            controller: 'HeaderCtrl',
            resolve: {currentUser: currentUser}
        };

        var user_list = {
            templateUrl: '/app/users/templates/index.html',
            controller: 'UserListCtrl',
            resolve: {currentUser: currentUser}
//            resolve: { allUsers: allUsers }
        };

        var user_edit = {
            templateUrl: '/app/users/templates/edit.html',
            controller: 'UserEditCtrl',
            resolve: {currentUser: currentUser}
        };

        var user_add = {
            templateUrl: '/app/users/templates/add.html',
            controller: 'UserAddCtrl',
            resolve: {currentUser: currentUser}
        };

        var resort_settings = {
            templateUrl: '/app/resorts/templates/settings.html',
            controller: 'ResortSettingsCtrl',
            resolve: {
                questions: questions,
                currentUser: currentUser
            }
        };

        var incidents = {
            templateUrl: '/app/incidents/templates/index.html',
            controller: 'IncidentCtrl',
            resolve: {
                currentUser: currentUser,
                questions: questions
            }
        };

        var incident_edit = {
            templateUrl: '/app/incidents/templates/edit.html',
            controller: 'IncidentUpdateCtrl',
            resolve: {
                questions: questions,
                currentUser: currentUser
            }
        };

        var dashboard = {
            templateUrl: '/app/analytics/templates/dashboard.html',
            controller: 'DashboardCtrl',
            resolve: {currentUser: currentUser}
        };

        var patrollers_report = {
            templateUrl: '/app/analytics/templates/patrollers_report.html',
            controller: 'PatrollersReportCtrl',
            resolve: {
                currentUser: currentUser,
                locations: locations
            }
        };

        var reporting = {
            templateUrl: '/app/analytics/templates/report.html',
            controller: 'ReportCtrl',
            resolve: {
                currentUser: currentUser,
                questions: questions
            }
        };

        var chart = {
            templateUrl: '/app/analytics/templates/chart.html',
            controller: 'ChartCtrl',
            resolve: {
                currentUser: currentUser,
                questions: questions
            }
        };

        var case_status = {
            templateUrl: '/app/analytics/templates/case_status.html',
            controller: 'CaseStatusCtrl',
            resolve: {
                currentUser: currentUser,
                incidentStatus: incidentStatus
            }
        };

        var geomap = {
            templateUrl: '/app/map/templates/map.html',
            controller: 'MapCtrl',
            resolve: {
                currentUser: currentUser,
                questions: questions,
                settings: resortSettings
            }
        };

        var heatmap = {
            templateUrl: '/app/map/templates/heatmap.html',
            controller: 'HeatmapCtrl',
            resolve: {
                currentUser: currentUser,
                settings: resortSettings
            }
        };

        var area_list = {
            templateUrl: '/app/areas/templates/index.html',
            controller: 'AreaListCtrl',
            resolve: {currentUser: currentUser}
        };

        var area_edit = {
            templateUrl: '/app/areas/templates/edit.html',
            controller: 'AreaEditCtrl',
            resolve: {currentUser: currentUser}
        };

        var area_add = {
            templateUrl: '/app/areas/templates/add.html',
            controller: 'AreaAddCtrl',
            resolve: {currentUser: currentUser}
        };

        var location_list = {
            templateUrl: '/app/locations/templates/index.html',
            controller: 'LocationListCtrl',
            resolve: {currentUser: currentUser}
        };

        var location_edit = {
            templateUrl: '/app/locations/templates/edit.html',
            controller: 'LocationEditCtrl',
            resolve: {currentUser: currentUser}
        };

        var location_add = {
            templateUrl: '/app/locations/templates/add.html',
            controller: 'LocationAddCtrl',
            resolve: {currentUser: currentUser}
        };

        var controlled_substances_list = {
            templateUrl: '/app/controlled_substances/templates/index.html',
            controller: 'ControlledSubstanceListCtrl',
            resolve: {currentUser: currentUser}
        };

        var controlled_substance_edit = {
            templateUrl: '/app/controlled_substances/templates/edit.html',
            controller: 'ControlledSubstanceEditCtrl',
            resolve: {currentUser: currentUser}
        };

        var controlled_substance_add = {
            templateUrl: '/app/controlled_substances/templates/add.html',
            controller: 'ControlledSubstanceAddCtrl',
            resolve: {currentUser: currentUser}
        };

        var asset_list = {
            templateUrl: '/app/assets/templates/index.html',
            controller: 'AssetListCtrl',
            resolve: {
                currentUser: currentUser,
                assetTypes: assetTypes
            }
        };

        var asset_edit = {
            templateUrl: '/app/assets/templates/edit.html',
            controller: 'AssetEditCtrl',
            resolve: {
                currentUser: currentUser,
                assetTypes: assetTypes,
                areas: areas,
                locations: locations
            }
        };

        var asset_add = {
            templateUrl: '/app/assets/templates/add.html',
            controller: 'AssetAddCtrl',
            resolve: {
                currentUser: currentUser,
                assetTypes: assetTypes,
                areas: areas,
                locations: locations
            }
        };

        var stock_add = {
            templateUrl: '/app/stocks/templates/add.html',
            controller: 'StockAddCtrl',
            resolve: {
                currentUser: currentUser,
                locations: locations,
                controlledSubstances:controlledSubstances
            }
        };

        var stock_checkout = {
            templateUrl: '/app/stocks/templates/checkout.html',
            controller: 'StockCheckoutCtrl',
            resolve: {
                currentUser: currentUser,
                locations: locations,
                controlledSubstances:controlledSubstances,
                questions: questions,
            }
        };

        var stock_report = {
            templateUrl: '/app/stocks/templates/report.html',
            controller: 'StockReportCtrl',
            resolve: {
                currentUser: currentUser,
                locations: locations,
                controlledSubstances:controlledSubstances
            }
        };

        var audit_log = {
            templateUrl: '/app/audit_log/templates/index.html',
            controller: 'AuditLogListCtrl',
            resolve: {currentUser: currentUser}
        };

        // States
        $stateProvider
            .state('login', {
                url: '/login',
                views: {
                    'content': login
                },
                authenticate: false
            })
            .state('password_forgot', {
                url: '/password/forgot',
                views: {
                    'content': password_forgot

                },
                authenticate: false
            })
            .state('password_reset', {
                url: '/password/reset',
                views: {
                    'content': password_reset
                },
                authenticate: false
            })
            .state('users', {
                url: '/users',
                views: {
                    'header': header,
                    'content': user_list

                },
                authenticate: true,
                allowedRoles: ['Manager']
            })
            .state('user_edit', {
                url: '/users/{userId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': user_edit

                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher']
            })

            .state('user_add', {
                url: '/users/add',
                views: {
                    'header': header,
                    'content': user_add

                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Manager']
            })

            .state('resort_settings', {
                url: '/resorts/{resortId:[0-9A-Za-z-]+}/settings',
                views: {
                    'header': header,
                    'content': resort_settings

                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Manager']
            })

            .state('incidents', {
                url: '/incidents',
                views: {
                    'header': header,
                    'content': incidents

                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher']
            })

            .state('incident_edit', {
                url: '/incidents/{incidentId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': incident_edit
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher']
            })

            .state('reporting', {
                url: '/reporting',
                views: {
                    'header': header,
                    'content': reporting

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('report_edit', {
                url: '/reporting/{reportId:[0-9A-Za-z-]+}/',
                views: {
                    'header': header,
                    'content': reporting

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('charts', {
                url: '/charts',
                views: {
                    'header': header,
                    'content': chart

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('case-status', {
                url: '/case-status',
                views: {
                    'header': header,
                    'content': case_status

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('chart_edit', {
                url: '/charts/{reportId:[0-9A-Za-z-]+}/',
                views: {
                    'header': header,
                    'content': chart

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('map', {
                url: '/map',
                views: {
                    'header': header,
                    'content': geomap
                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

            .state('heatmap', {
                url: '/heatmap',
                views: {
                    'header': header,
                    'content': heatmap

                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })
            .state('areas', {
                url: '/areas',
                views: {
                    'header': header,
                    'content': area_list

                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })
            .state('area_edit', {
                url: '/areas/{areaId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': area_edit

                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('area_add', {
                url: '/areas/add',
                views: {
                    'header': header,
                    'content': area_add
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('locations', {
                url: '/locations?areaId',
                views: {
                    'header': header,
                    'content': location_list
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })
            .state('location_edit', {
                url: '/locations/{locationId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': location_edit
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('location_add', {
                url: '/locations/add',
                views: {
                    'header': header,
                    'content': location_add
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('controlled_substances', {
                url: '/controlled-substances',
                views: {
                    'header': header,
                    'content': controlled_substances_list
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })
            .state('controlled_substance_edit', {
                url: '/controlled-substances/{controlledSubstanceId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': controlled_substance_edit
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('controlled_substance_add', {
                url: '/controlled-substances/add',
                views: {
                    'header': header,
                    'content': controlled_substance_add
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('assets', {
                url: '/assets',
                views: {
                    'header': header,
                    'content': asset_list
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('asset_edit', {
                url: '/assets/{assetId:[0-9A-Za-z-]+}/edit',
                views: {
                    'header': header,
                    'content': asset_edit
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('asset_add', {
                url: '/assets/add',
                views: {
                    'header': header,
                    'content': asset_add
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_asset_management'
            })

            .state('stock_add', {
                url: '/stock/add',
                views: {
                    'header': header,
                    'content': stock_add
                },
                resolve: {
                    currentUser: currentUser,
                    controlledSubstances: controlledSubstances,
                    locations:locations
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('stock_checkout', {
                url: '/stock/checkout?controlledSubstanceStockId&controlledSubstanceId&locationId',
                views: {
                    'header': header,
                    'content': stock_checkout
                },
                resolve: {
                    currentUser: currentUser,
                    controlledSubstances: controlledSubstances,
                    locations:locations
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('stock_report', {
                url: '/stock/report',
                views: {
                    'header': header,
                    'content': stock_report
                },
                resolve: {
                    currentUser: currentUser
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('audit_log', {
                url: '/audit',
                views: {
                    'header': header,
                    'content': audit_log
                },
                authenticate: true,
                allowedRoles: ['Patroller', 'Manager', 'Dispatcher'],
                allowedPermissions: 'user_controlled_substances'
            })

            .state('dashboard', {
                url: '/',
                views: {
                    'header': header,
                    'content': dashboard
                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })
            .state('patrollers_report', {
                url: '/reports/patrollers',
                views: {
                    'header': header,
                    'content': patrollers_report
                },
                resolve: {
                    currentUser: currentUser,
                    locations:locations
                },
                authenticate: true,
                allowedRoles: ['Manager', 'Dispatcher']
            })

        ;
    })

    .run(function ($rootScope, $http, $cookies, $state, $stateParams, $window, $sce, $translate, $log, Idle, growl, UserService, LS, $modal, hotkeys, $intercom) {
        // start watching when the app runs. also starts the $keepalive service by default.
        $rootScope.$on('IdleStart', function () {
            if ($rootScope.warning) {
                $rootScope.warning.hide();
                $rootScope.warning = null;
            }

            $rootScope.warning = $modal({
                title: "Session Timeout",
                content: "You'll be logged out in 2 minutes."
            });
        });

        $rootScope.$on('IdleEnd', function () {
            if ($rootScope.warning) {
                $rootScope.warning.hide();
                $rootScope.warning = null;
            }
        });

        $rootScope.$on('IdleTimeout', function () {
            // the user has timed out (meaning idleDuration + warningDuration has passed without any activity)
            if ($rootScope.warning) {
                $rootScope.warning.hide();
                $rootScope.warning = null;
            }

            // this is where you'd log them
            $intercom.shutdown();
            UserService.logout(0)
                .then(function (data) {
                    LS.clear();
                    $state.transitionTo('login');
                }, function (error) {
                    $log.log(error);
                });
        });

        Idle.watch();

//        $rootScope.online = navigator.onLine;
//
//        $window.addEventListener("offline", function() {
//            $rootScope.$apply(function() {
//                $rootScope.online = false;
//            });
//        }, false);
//
//        $window.addEventListener("online", function() {
//            $rootScope.$apply(function() {
//                $rootScope.online = true;
//            });
//        }, false);

//    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;


        $rootScope.$on("$stateChangeStart",
            function (event, toState, toParams, fromState, fromParams) {
                if (toState.authenticate && !UserService.is_authenticated) {
                    $state.transitionTo('login');
                    event.preventDefault();
                } else {
                    if (toState.hasOwnProperty('allowedRoles')) {
                        if (UserService.currentRole() && $.inArray(UserService.currentRole(), toState.allowedRoles) >= 0) {

                            //check permission
                            var user = UserService.currentUser();

                            if(toState.hasOwnProperty('allowedPermissions')){
                                if(user.hasOwnProperty(toState.allowedPermissions) && user[toState.allowedPermissions]){

                                }else{
                                    if (UserService.currentRole() == "Patroller") {
                                        $state.transitionTo('incidents');
                                    }
                                    else {
                                        $state.transitionTo('map');
                                    }
                                    $log.log("Permission denied");
                                    event.preventDefault();
                                }
                            }
                        } else {
                            if (UserService.currentRole() == "Patroller") {
                                $state.transitionTo('incidents');
                            }
                            else {
                                $state.transitionTo('map');
                            }
                            $log.log("Permission denied");
                            event.preventDefault();
                        }

                    }
                }
            });

        hotkeys.bindTo($rootScope).add({
            combo: 'shift+m',
            description: 'Toggle menu',
            callback: function () {
                $rootScope.siderbtn = !$rootScope.siderbtn;
            },
            persistent: true
        });

        $rootScope.stripurl = function (url) {
            // strips off the http:// and / off the end of urls
            var r = /https?\:\/\/(.+)\//;
            return r.test(url) ? r.exec(url)[1] : url;
        };

        $rootScope.safeHtml = function (val) {
            return $sce.trustAsHtml(val);
        };

        $rootScope.changeLanguage = function (key) {
            $translate.use(key);
        };

        //Unit conversion
        $rootScope.KM2M = function (value) {
            return Math.round(value * 0.621 * 10) / 10;
        };

        $rootScope.M2KM = function (value) {
            return Math.round(value * 1.609 * 10) / 10;
        };

        $rootScope.M2FT = function (value) {
            return Math.round(value * 3.2808 * 10) / 10;
        };

        $rootScope.FT2M = function (value) {
            return Math.round(value * 0.3048 * 10) / 10;
        };

        $rootScope.KM2FT = function (value) {
            var m = Math.round(value * 0.621 * 10) / 10;
            return $rootScope.M2FT(m);
        };

        $rootScope.FT2KM = function (value) {
            var m = Math.round(value * 0.3048 * 10) / 10;
            return $rootScope.M2KM(m);
        };

        $rootScope.C2F = function (value) {
            return Math.round((value * 1.8 + 32) * 10) / 10;
        };

        $rootScope.F2C = function (value) {
            return Math.round(((value - 32) / 1.8) * 10) / 10;
        };

        $rootScope.KG2LB = function (value) {
            return Math.round(value * 2.205 * 10) / 10;
        };

        $rootScope.LB2KG = function (value) {
            return Math.round(value * 0.453 * 10) / 10;
        };

        $rootScope.isAuthenticated = function () {
            return !($rootScope.user == null || $rootScope.user == undefined );
        };

        $rootScope.toUTC = function (value) {
            var tz = jstz.determine();
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        };

        $rootScope.toLocalTime = function (value) {
            var tz = jstz.determine();
            return moment.utc(value).tz(tz.name()).format('YYYY-MM-DD HH:mm:ss');
        };

        $rootScope.on_error = function (reason) {
            $log.log(reason);
//
//        if (reason.errors.Error.indexOf("expired") !== -1) {
//            $log.log('expired');
//            $state.transitionTo('login');
//        }
        };

//
//    $rootScope.hasRole = function (role) {
//        return ($rootScope.isAuthenticated() && $rootScope.user.Role[0] == role)
//    };

//    $state.errorGo = function (to, parms) {
//        return $state.transitionTo(to, parms, {location: false, inherit: true, relative: $state.$current, notify: true});
//    };
    });

angular.module('app.services', []);
