'use strict';


angular.module('app')
    .controller('ControlledSubstanceAddCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, ControlledSubstanceService, currentUser, growl) {
        $scope.add = function () {
            growl.info("ADD_CONTROLLED_SUBSTANCE");

            ControlledSubstanceService.add($scope.controlled_substance_name, $scope.units).then(function (data) {
                    growl.success("controlled_substance_created_successfully");
                    $state.go("controlled_substances");
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
