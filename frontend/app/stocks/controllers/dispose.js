'use strict';

angular.module('app')
    .controller('StockDisposeCtrl', function ($scope, $location, $state, $rootScope, $timeout, $q, $log, $stateParams, $intercom, $modalInstance, StockService, data, growl, controlledSubstances, locations) {

        $scope.data = data;

        $scope.ok = function () {
            $q.all(_.map(data, function (item) {
                var deferred = $q.defer();
                StockService.dispose(item.controlled_substance_stock_id).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    growl.error(error.detail);
                    deferred.reject(error);
                });

                return deferred.promise;
            })).then(function (response) {
                $modalInstance.close(true);
            });
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
