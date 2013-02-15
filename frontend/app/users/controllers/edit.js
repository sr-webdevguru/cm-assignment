'use strict';


angular.module('app')
    .controller('UserEditCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, UserService, currentUser, growl) {

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

        $scope.showRole = false;
        $scope.showPermissions = currentUser.resorts[0].resort_controlled_substances || currentUser.resorts[0].resort_asset_management;
        $scope.showDeleteUser = false;
        $scope.showActivateUser = false;
        $scope.showDeactivateUser = false;

        var id = $stateParams.userId;


        $scope.roles = [
            {key: 1, name: 'Patroller'},
            {key: 2, name: 'Dispatcher'},
            {key: 3, name: 'Manager'}
        ];

        $scope.get = function () {
            if (id) {
                growl.info("LOADING_USER");
                UserService.fetch(id).then(function (data) {
//                        $log.log(data);
                        $scope.user = data;
                        $scope.user.role = data.role_id[0].value;

                        if (currentUser.user_id != data.user_id && currentUser.role == 'Manager'){
                            $scope.showRole = true;
                            $scope.showDeleteUser = true;
                            $scope.showActivateUser = data['user_status'] == 1;
                            $scope.showDeactivateUser = data['user_status'] == 0;
                        }
                        growl.info("LOADING_DEVICES");
                        UserService.fetchDevices(id).then(function (data) {

//                                $log.log(data);
                                $scope.user.devices = data.devices;
                            },
                            $rootScope.on_error);
                    },
                    function(error){
                        growl.info(error.detail);
                    }
                );
            }
        };

        $scope.saveUser = function () {
            if (id) {
                growl.info("SAVE_USER");
                UserService.saveUser(id, $scope.user.name, $scope.user.email, $scope.user.role, $scope.user.phone, $scope.user.user_asset_management, $scope.user.user_controlled_substances).then(function (data) {
//                        $log.log(data);
                        growl.success("user_updated_successfully");
                    },
                    function(error){
//                        growl.info(error.detail);

                        //Global errors
                    if (error.hasOwnProperty('detail')) {
                        $scope.error = error.detail;
                        $scope.form.$setPristine();
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
            }
        };

        $scope.resetPassword = function () {
                growl.info("RESET_PASSWORD");
                UserService.forgotPassword($scope.user.email)
                    .then(function (data) {
                        growl.success(data.detail);
                    }, function (error) {
                        growl.error(error.detail);
                    });
        };

        $scope.removeUser = function () {
            if (id) {
                growl.info("REMOVE_USER");
                UserService.removeUser(id, $scope.user.firstname, $scope.user.lastname, $scope.user.email).then(function (data) {
                        growl.success("REMOVE_USER");
                        $state.go("users");
                    },
                    function(error){
                        growl.info(error.detail);
                    });
            }
        };

        $scope.toggleUserStatus = function(type){
            UserService.updateUserStatus($scope.user.user_id, $scope.user.resorts[0]['resort_id'], type).then(function (data) {
                    growl.success(data);
                    $scope.showActivateUser = type == 'archived' ? true : false;
                    $scope.showDeactivateUser = type == 'archived' ? false : true;
                },
                function(error){
                    growl.info(error.detail);
                });
        };

        $scope.testNotifications = function (deviceId) {
            if (deviceId) {
                growl.info("TEST_NOTIFICATIONS");
                UserService.testDevice(deviceId).then(function (data) {
                        growl.success(data);
                    },
                    function(error){
                        growl.info(error.detail);
                    });
            }
        };

        $scope.removeDevice = function (deviceId) {
//            $log.log(deviceId);

            if (deviceId) {
                growl.info("REMOVE_DEVICE");
                UserService.removeDevice(deviceId).then(function (data) {
//                        $log.log(data);
                        growl.success("DEVICE_REMOVED");
                        $scope.get();
                    },
                   function(error){
                        growl.info(error.detail);
                    });
            }
        };


    });