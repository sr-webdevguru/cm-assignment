'use strict';


angular.module('app')
    .controller('AssetEditCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AssetService, currentUser, assetTypes, areas, locations, growl) {
        var id = $stateParams.assetId;

        $scope.assetTypes = assetTypes.results;
        //$scope.asset_type_id = $scope.assetTypes[0].asset_type_id;

        $scope.areas = areas.results;
        //$scope.area_id = $scope.areas[0].area_id;

        var allLocations = locations.results;

        function refreshLocations(area_id, location_id) {
            $scope.locations = _.filter(allLocations, function (location) {
                return location.area.area_id == area_id;
            });

            var location = _.find(allLocations, function (location) {
                return location.area.area_id == $scope.area_id;
            });

            if(location_id){
                $scope.asset.location_id = location_id;
            }else {
                if (location) {
                    $scope.asset.location_id = location.location_id;
                } else {
                    $scope.asset.location_id = null;
                }
            }
        }

        $scope.$watch('asset.area_id', function (newValue, oldValue) {
            if (newValue && newValue != oldValue) {
                refreshLocations(newValue, $scope.asset.location_id);
            }
        });

        $scope.get = function () {
            if (id) {
                growl.info("LOADING_ASSET");
                AssetService.fetch(id).then(function (data) {
                        $scope.asset = data;

                        if($scope.asset.asset_type) {
                            $scope.asset.asset_type_id = data.asset_type.asset_type_id;
                        }

                        if($scope.asset.location) {
                            $scope.asset.area_id = data.location.area.area_id;
                            $scope.asset.location_id = data.location.location_id;

                            refreshLocations($scope.asset.area_id, $scope.asset.location_id);
                        }
                    },
                    function (error) {
                        growl.info(error.detail);
                    }
                );
            }
        };

        $scope.update = function () {
            if (id) {
                growl.info("UPDATE_ASSET");
                AssetService.update(id, $scope.asset.asset_name, $scope.asset.asset_type_id, $scope.asset.location_id).then(function (data) {
//                        $log.log(data);
                        growl.success("asset_updated_successfully");
                    },
                    function (error) {
                        growl.info(error.detail);
                    });
            }
        };

    });
