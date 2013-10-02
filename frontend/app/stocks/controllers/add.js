'use strict';


angular.module('app')
    .controller('StockAddCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, StockService, currentUser, controlledSubstances, locations, growl) {

        $scope.controlled_substances = controlledSubstances.results;

        $scope.locations = locations.results;

        $scope.add = function () {
            growl.info("ADD_ASSET");

            StockService.add($scope.quantity, $scope.controlled_substance.controlled_substance_id, $scope.volume,
                $scope.location_id, $scope.dt_expiry).then(function (data) {
                    growl.success("stock_added_successfully");
                    $state.go("stock_report");
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
