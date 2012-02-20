'use strict';


angular.module('app')
    .controller('AreaListCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'AreaService', 'currentUser', 'growl', '$uimodal', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AreaService, currentUser, growl, $modal) {

        $scope.list = {
            items: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'area_name',
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
                AreaService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, '', $scope.list.predicate, $scope.list.reverse)
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

            archive: function(area_id) {
                console.log("removing");

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/areas/templates/confirm.html',
                    controller: 'ConfirmModalCtrl',
                    size: 'md'
                });

                modalInstance.result.then(function () {
                    AreaService.remove(area_id).then(function (response) {
                        $scope.list.get();
                    }, function (error) {
                        growl.error(error.detail);
                    });

                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                });
            },

            search: function (text) {
                $scope.list.loading = true;

                growl.info("LOADING_AREA");

                AreaService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, text, $scope.list.predicate, $scope.list.reverse)
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
            }
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
