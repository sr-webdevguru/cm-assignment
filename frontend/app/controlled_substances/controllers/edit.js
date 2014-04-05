'use strict';


angular.module('app')
    .controller('ControlledSubstanceEditCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, ControlledSubstanceService, currentUser, growl) {
        var id = $stateParams.controlledSubstanceId;

        $scope.get = function () {
            if (id) {
                growl.info("LOADING_CONTROLLED_SUBSTANCE");

                ControlledSubstanceService.fetch(id).then(function (data) {
                        $scope.controlled_substance = data;
                    },
                    function (error) {
                        growl.info(error.detail);
                    }
                );
            }
        };

        $scope.update = function () {
            if (id) {
                growl.info("UPDATE_CONTROLLED_SUBSTANCE");
                ControlledSubstanceService.update(
                    id, $scope.controlled_substance.controlled_substance_name, $scope.controlled_substance.units)
                    .then(function (data) {
//                        $log.log(data);
                        growl.success("controlled_substance_updated_successfully");
                    },
                    function (error) {
                        growl.info(error.detail);
                    });
            }
        };

    });
