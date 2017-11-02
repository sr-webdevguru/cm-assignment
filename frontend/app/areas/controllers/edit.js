'use strict';


angular.module('app')
    .controller('AreaEditCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AreaService, currentUser, growl) {
        var id = $stateParams.areaId;

        $scope.get = function () {
            if (id) {
                growl.info("LOADING_AREA");
                AreaService.fetch(id).then(function (data) {
                        $scope.area = data;
                    },
                    function (error) {
                        growl.info(error.detail);
                    }
                );
            }
        };

        $scope.updateArea = function () {
            if (id) {
                growl.info("UPDATE_AREA");
                AreaService.update(id, $scope.area.area_name).then(function (data) {
//                        $log.log(data);
                        growl.success("area_updated_successfully");
                    },
                    function (error) {
                        growl.info(error.detail);
                    });
            }
        };

    });
