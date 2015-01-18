'use strict';


angular.module('app')
    .controller('LocationListCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'LocationService', 'AreaService', 'currentUser', 'growl', '$uimodal', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, LocationService, AreaService, currentUser, growl, $modal) {


        var areaId='';

        if($stateParams.hasOwnProperty('areaId') && $stateParams.areaId) {
            areaId = $stateParams.areaId;
        }

        AreaService.fetchAll(1000, 0, '', 'area_name', 'asc')
            .then(function (data) {
                $scope.areas = data.results;
            },
            function (error) {
                growl.error(error.detail);
            }
        )
            .finally(function () {
                $scope.areas.unshift({
                    area_id:'__empty__',
                    area_name:'All Areas'
                });

                $scope.area_id=areaId;

                $scope.list.get();
            });

        $scope.list = {
            items: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'location_name',
            loading: false,

            setPage: function (pageNum) {
                $scope.list.currentPage = pageNum;
            },

            filter: function () {
                $timeout(function () {
                    $scope.list.filteredItems = $scope.list.filtered.length;
                    $scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }, 10);
            },

            sort_by: function (predicate) {
                $scope.list.predicate = predicate;
                $scope.list.reverse = !$scope.list.reverse;

                $scope.list.get();
            },

            get: function () {
                $log.log('fetching items...');
                $scope.list.loading = true;

                growl.info("LOADING_AREA");

                var area_id = $scope.area_id;
                if($scope.area_id == '__empty__'){
                    area_id = '';
                }

                LocationService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, '',area_id, $scope.list.predicate, $scope.list.reverse)
                    .then(function (data) {
                        $scope.list.items = data.results;
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);
                    },
                    function (error) {
                        growl.error(error.detail);
                    }
                )
                    .finally(function () {
                        $scope.list.loading = false;
                    });
            },

            search: function (text) {
                $scope.list.loading = true;

                growl.info("LOADING_AREA");

                LocationService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, text, $scope.list.predicate, $scope.list.reverse)
                    .then(function (data) {
                        $scope.list.items = data.results;
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);
                    },
                    function (error) {
                        growl.error(error.detail);
                    }
                )
                    .finally(function () {
                        $scope.list.loading = false;
                    });
            },

            archive: function(id) {
                console.log("removing");

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/locations/templates/confirm.html',
                    controller: 'ConfirmModalCtrl',
                    size: 'md'
                });

                modalInstance.result.then(function () {
                    LocationService.remove(id).then(function (response) {
                        $scope.list.get();
                    }, function (error) {
                        growl.error(error.detail);
                    });

                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                });
            }
        };

        $scope.add = function () {
            $state.go("user_add");
        };

        $scope.$watch(
            'list.itemsPerPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        $scope.$watch(
            'list.currentPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        $scope.$watch(
            'area_id',
            function (newValue, oldValue) {
                if (newValue && newValue !== oldValue) {
                    $state.go('locations', {areaId:newValue});
                }
            }
        );

        var filterTextTimeout;

        $scope.$watch(
            'search',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {

                    if (filterTextTimeout) {
                        $timeout.cancel(filterTextTimeout);
                    }

                    filterTextTimeout = $timeout(function () {
                        console.log("value changed");
                        $scope.list.search(newValue);
                    }, 1000); // delay 250 ms


                }
            }
        );
    }]);
