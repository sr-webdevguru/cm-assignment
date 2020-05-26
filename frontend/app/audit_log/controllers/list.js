'use strict';


angular.module('app')
    .controller('AuditLogListCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'AuditLogService', 'currentUser', 'growl', '$uimodal', 'DateRangeService', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, AuditLogService, currentUser, growl, $modal, DateRangeService) {

        var current = new Date();
        var tz = jstz.determine();

        function toUTC(value) {
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format('YYYY-MM-DD HH:mm:ss');
        }

        $scope.list = {
            items: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'dt_added',
            loading: false,
            dateFrom: moment(DateRangeService.range.dateFrom).format('YYYY-MM-DD'),
            dateTo: moment(DateRangeService.range.dateTo).format('YYYY-MM-DD'),

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

                var start_time = toUTC(moment($scope.list.dateFrom).format('YYYY-MM-DD 00:00:00'));
                var end_time = toUTC(moment($scope.list.dateTo).format('YYYY-MM-DD 23:59:59'));

                AuditLogService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, '', $scope.list.predicate, $scope.list.reverse, start_time, end_time)
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

                AuditLogService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, text, $scope.list.predicate, $scope.list.reverse)
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

            archive: function(areaId) {
                console.log("removing");

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/areas/templates/confirm.html',
                    controller: 'ConfirmModalCtrl',
                    size: 'md'
                });

                modalInstance.result.then(function () {
                    AuditLogService.remove(areaId).then(function (response) {
                        $scope.list.get();
                    }, function (error) {
                        growl.error(error.detail);
                    });

                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                });
            }
        };

        $scope.$watch(
            'list.dateFrom',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                }
            }
        );

        $scope.$watch(
            'list.dateTo',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                }
            }
        );

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
