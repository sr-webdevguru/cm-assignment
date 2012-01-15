'use strict';

angular.module('app')
    .controller('AuthCtrl', ['$scope', '$location', '$state', '$timeout', '$rootScope', '$log', 'UserService', 'LS', 'CONFIG', '$http', 'ApiService', function ($scope, $location, $state, $timeout, $rootScope, $log, UserService, LS, CONFIG, $http, ApiService) {

        $scope.form = {
            errors: null
        };

        var ENV_MAPPING = {
            'X': '-',
            'Y': '-dev-',
            'Z': '-staging-'
        };

        var COUNTRY_MAPPING = {
            1: 'us',
            2: 'au',
            3: 'ca'
        };

        if ($location.path().split('/')[2] == "reset") {
            var token = $location.search().token;
            if (token) {
                $scope.message = "";
                var server_id = token.split('-')[3];
                $scope.uid = token.split('-')[0];
                $scope.token = token.split('-')[1] + "-" + token.split('-')[2];
                $scope.url = "https://api" + ENV_MAPPING[server_id[0]] + COUNTRY_MAPPING[server_id[1]] + ".medic52.com/reset/" + $scope.uid + "/" + $scope.token + "/";
            }
            else {
                $state.transitionTo('login');
            }
        }

        $scope.init = function () {
            var email = '';
            var remember_me = false;

            if (LS.get('remember_me') == 'true') {
                email = LS.get('user_email');
                remember_me = true;
            }

            $scope.user = {
                email: email,
                password: '',
                remember_me: remember_me
            };
        };

        $scope.login = function () {
            if (UserService.is_authenticated) {

                //Transition to List incident if patroller else go to map
                if (UserService.currentRole() == "Patroller") {
                    $state.transitionTo('incidents');
                }
                else {
                    $state.transitionTo('map');
                }


            } else {

                LS.set('remember_me', $scope.user.remember_me);

                if ($scope.user.remember_me == true) {
                    LS.set('user_email', $scope.user.email);
                }
                else {
                    LS.set('user_email', '');
                }

                UserService.discover($scope.user.email)
                    .then(function (response) {

                        UserService.login($scope.user.email, $scope.user.password)
                            .then(function (data) {

                                $http({
                                    method: 'GET',
                                    url: ApiService.laravel() +
                                        '/laracors?authorization=' + data.user.token +
                                        '&token=' + LS.get('token'),
                                    data: {
                                        authorization: data.user.token,
                                        token: LS.get('token')
                                    }
                                });
                                $log.log(data.user.role);

                                //Transition to List incident if patroller else go to map
                                if (data.user.role == "Patroller") {
                                    $state.transitionTo('incidents');
                                }
                                else {
                                    $state.transitionTo('map');
                                }

                            }, function (error) {
                                $scope.form.errors = error.detail;
                                $scope.init();
                            });
                    });
            }
        };

        $scope.show_forgot_password = function () {
            $state.transitionTo('password_forgot');
        };

        $scope.send_reset_password = function () {

            if ($scope.user.email) {
                UserService.forgotPassword($scope.user.email)
                    .then(function (data) {
//                        $log.log(data);
                        $scope.form.success = data.detail;
                        //$state.transitionTo('login');
                    }, function (error) {
                        $scope.form.errors = error.detail;

                        $scope.init();
                    });
            }

        };

        $scope.submit = function () {

            if ($scope.password1 != $scope.password2) {
                $scope.message = "Password and repeat password do not match";
                $scope.password1 = "";
                $scope.password2 = "";
            }
            else {
                $http({
                    method: 'POST',
                    url: $scope.url,
                    data: $.param({"new_password1": $scope.password1, "new_password2": $scope.password2}),  // pass in data as strings
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}  // set the headers so angular passing info as form data (not request payload)
                })
                    .success(function (data) {
                        $scope.message = "Password Reset Successful. You can now login";
                        $scope.password1 = "";
                        $scope.password2 = "";
                        $timeout(function () {
                            $state.transitionTo('login');
                        }, 3000);
                    }).error(function (data) {
                        $scope.message = "Password reset link has expired (or) invalid";
                        $scope.password1 = "";
                        $scope.password2 = "";
                    });
            }
        };

    }]);


