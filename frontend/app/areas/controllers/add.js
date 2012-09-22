'use strict';


angular.module('app')
    .controller('AreaAddCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AreaService, currentUser, growl) {
        $scope.addArea = function () {
            growl.info("ADD_AREA");

            AreaService.add($scope.area_name).then(function (data) {
                    growl.success("area_created_successfully");
                    $state.go("areas");
                },
                function (error) {
                    growl.info(error.detail);

                    //Global errors
                    //if (error.hasOwnProperty('detail')) {
                    //    $scope.error = error.detail;
                    //    $scope.form.$setPristine();
                    //    growl.error(error.detail);
                    //}
                    //
                    //$scope.errors = [];
                    //angular.forEach(error, function (errors, field) {
                    //
                    //    if (field == 'non_field_errors') {
                    //        // Global errors
                    //        $scope.error = errors.join(', ');
                    //        $scope.form.$setPristine();
                    //    } else {
                    //        //Field level errors
                    //        $scope.form[field].$setValidity('backend', false);
                    //        $scope.form[field].$dirty = true;
                    //        $scope.errors[field] = errors.join(', ');
                    //    }
                    //});
                });
        };
    });
