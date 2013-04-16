'use strict';

angular.module('app')
    .controller('HeaderCtrl', function ($scope, $location, $state, $log, $sce, $intercom, hotkeys, UserService, LS, ReportService) {
        //state-title mapping

        var states = {
            dashboard: 'Dashboard',

            map: 'Map',
            heatmap: 'Heatmap',
            patrollers_report: 'Patrollers',
            incidents: 'Incidents',
            incident_edit: 'Incidents',

            users: 'Users',
            user_edit: 'Users',
            user_add: 'Users',
            reporting: 'Reports',
            charts: 'Charts'
        };
        var laravelHost = LS.get('LARAVEL_CORS');
        var access_token = LS.get('Authorization') && LS.get('Authorization').split(' ').length > 1?
            LS.get('Authorization').split(' ')[1] : ''
        var query = '?authorization=' + LS.get('token').split(' ')[1] + '&bearer=' + access_token;
        var laravel = {
            home: laravelHost + query,
            due_today: laravelHost + '/assets/due-today' + query,
            assets: laravelHost + '/assets' + query,
            controlled_substances: laravelHost + '/controlled-substances' + query,
            areas: laravelHost + '/areas' + query,
            locations: laravelHost + '/locations' + query,
        };
        $scope.goTo = function(route){
            console.log(laravel[route]);
            window.location = laravel[route];
        };
//        $scope.$watch('online', function(isOnline) {
//            $log.log(isOnline);
//
//            if(!isOnline){
//                growl.info('we_are_trying_to_connect');
//            }
//        });

        $scope.page_title = states[$state.current.name];
        $scope.currentUser = UserService.currentUser();
        $scope.roles = ['', 'Patroller', 'Dispatcher', 'Manager'];
        $scope.currentUser.role = $scope.roles[$scope.currentUser.role_id[0].value];
        $scope.currentUser.role_id.forEach(function (entry) {
            if (entry.value == 3) {
                $scope.currentUser.isManager = true;
            }
        });

        $scope.resort_logo = $sce.trustAsResourceUrl($scope.currentUser.resorts[0].resort_logo);
//        $log.log(currentUser);

        $scope.menu = [
//            {
//                'title': 'Home',
//                'link': '/'
//            }
        ];

        $scope.isCollapsed = true;

        $scope.isActive = function (route) {
            return route === $location.path();
        };

        $scope.isDesktop = (window.screen.width >= 992 );
        $scope.isPhone = (window.screen.width <= 992);

        $scope.logout = function () {
            $intercom.shutdown();
            UserService.logout(0)
                .then(function (data) {
                    LS.clear();
                    $state.transitionTo('login');
                }, function (error) {
                    $log.log(error);
                });
        };


        $intercom.boot({
            email: $scope.currentUser.email,
            name: $scope.currentUser.name,
            created_at: new Date(),
            user_id: $scope.currentUser.user_id,
            company: {
                id: $scope.currentUser.resorts[0].resort_id,
                name: $scope.currentUser.resorts[0].resort_name
            },
            role: $scope.currentUser.role_id[0].key,
            custom_launcher_selector: ".intercom-icon"
        });

        $scope.intercom_toggle = function () {
            $intercom.show();
//             if ($scope.intercom_open == undefined || $scope.intercom_open == null || !$scope.intercom_open) {
//
//             } else {
//                 $intercom.hide();
//             }
        };

        $scope.$on('reports-updated', function (event, args) {
            getReports();
        });

        getReports();

        function getReports() {
            ReportService.fetchAll().then(function (data) {
                $scope.reports = _.filter(data.results, function (result) {
                    return result.type == null;
                });
                $scope.charts = _.filter(data.results, function (result) {
                    return result.type != null;
                });
            }, function (error) {
                $log.log(error);
            });
        }

    });
