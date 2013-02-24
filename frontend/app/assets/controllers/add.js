'use strict';


angular.module('app')
    .controller('AssetAddCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AssetService, currentUser, assetTypes, areas, locations, growl) {

        $scope.assetTypes = assetTypes.results;
        $scope.asset_type_id = $scope.assetTypes[0].asset_type_id;

        $scope.areas = areas.results;
        $scope.area_id = $scope.areas[0].area_id;

        var allLocations = locations.results;

        refreshLocations($scope.area_id);

        function refreshLocations(area_id) {
            $scope.locations = _.filter(allLocations, function (location) {
                return location.area.area_id == area_id;
            });

            var location = _.find(allLocations, function (location) {
                return location.area.area_id == $scope.area_id;
            });

            if (location) {
                $scope.location_id = location.location_id;
            }else{
                $scope.location_id = null;
            }
        }

        $scope.$watch('area_id', function (newValue, oldValue) {
            if (newValue && newValue != oldValue) {
                refreshLocations($scope.area_id);
            }
        });

        $scope.add = function () {
            growl.info("ADD_ASSET");

            AssetService.add($scope.asset_name, $scope.asset_type_id, $scope.area_id, $scope.location_id).then(function (data) {
                    growl.success("asset_created_successfully");
                    $state.go("assets");
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
