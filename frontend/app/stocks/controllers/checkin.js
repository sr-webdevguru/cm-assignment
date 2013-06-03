'use strict';

angular.module('app')
    .controller('StockCheckinCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, $modalInstance, StockService, data, growl, controlledSubstances, locations) {

        $scope.data = data;

        $scope.controlled_substances = controlledSubstances.results;
        $scope.locations = locations.results;
        //_.filter(locations.results, function (location) {
        //    return location.location_id != data.location.location_id;
        //});

        $scope.ok = function (location_id) {
            StockService.checkin(data.assignment.controlled_substance_stock_assignment_id, location_id)
                .then(function (data) {
                },
                function (error) {
                    growl.error(error.detail);
                }
            );

            $modalInstance.close(true);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
