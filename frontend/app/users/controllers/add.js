'use strict';


angular.module('app')
    .controller('UserAddCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, UserService, currentUser, growl) {

        $intercom.update({
            email: currentUser.email,
            name: currentUser.name,
            created_at: new Date(),
            user_id: currentUser.user_id,
            company: {
                id: currentUser.resorts[0].resort_id,
                name: currentUser.resorts[0].resort_name
            },
            role: currentUser.role_id[0].key,
            dashboard_feature_last_used: "Users"
        });

        if (!currentUser.isManager) {
            $state.go("map");
        }

        $scope.roles = [
            {key: 1, name: 'Patroller'},
            {key: 2, name: 'Dispatcher'},
            {key: 3, name: 'Manager'}
        ];

        $scope.addUser = function () {
            growl.info("ADD_USER");
            UserService.addUser($scope.name, $scope.email, $scope.phone, $scope.role).then(function (data) {
//                    $log.log(data);
                    growl.success("user_created_successfully");
                    $state.go("users");
                },
                function (error) {
//                    growl.info(error.detail);
                    //Global errors
                    if (error.hasOwnProperty('detail')) {
                        $scope.error = error.detail;
                        $scope.form.$setPristine();
                        growl.error(error.detail);
                    }

                    $scope.errors = [];
                    angular.forEach(error, function (errors, field) {

                        if (field == 'non_field_errors') {
                            // Global errors
                            $scope.error = errors.join(', ');
                            $scope.form.$setPristine();
                        } else {
                            //Field level errors
                            $scope.form[field].$setValidity('backend', false);
                            $scope.form[field].$dirty = true;
                            $scope.errors[field] = errors.join(', ');
                        }
                    });
                });
        };
    });