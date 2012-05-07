'use strict';


angular.module('app')
    .controller('StockRelocateCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, $modalInstance, StockService, data, controlledSubstances, locations, growl) {

        $scope.data = data;

        $scope.locations = angular.copy(locations.results);

        $scope.ok = function (location_id) {
            _.each(data, function (item) {
                StockService.relocate(item.controlled_substance_stock_id, location_id).then(function (response) {

                }, function (error) {
                    growl.error(error.detail);
                });
            });

            $modalInstance.close(true);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
