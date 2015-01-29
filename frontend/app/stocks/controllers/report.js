'use strict';


angular.module('app')
    .controller('StockReportCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'StockService', 'currentUser', 'growl', '$uimodal', '$translate', 'locations', 'controlledSubstances', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, StockService, currentUser, growl, $modal, $translate, locations, controlledSubstances) {

        var current = new Date();
        var diff = new Date(current.getTime() - (30 * 24 * 60 * 60 * 1000)); // a month

        var tz = jstz.determine();

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        var date_format = $scope.datetime_format.slice(0,10);
        $scope.date_format = date_format_mapping[date_format];

        function toUTC(value) {
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format('YYYY-MM-DD HH:mm:ss');
        }


        $scope.css = "height:175px;background-color:transparent;";

        var statuses = {
            'in': 'in_stock',
            'out': 'allocated',
            'used': 'used'
        };

        //default = In Stock view
        $scope.current_status = 'in';
        $scope.current_status_text = statuses[$scope.current_status];

        $scope.bulk_actions = [{
            key: 'dispose',
            value: $translate.instant('dispose')
        }
        ];

        if (locations.results.length > 1) {
            $scope.bulk_actions.push({
                key: 'relocate',
                value: $translate.instant('relocate')
            })
        }

        $scope.locations = angular.copy(locations.results);
        $scope.locations.unshift({
            location_id: '__empty__',
            location_name: 'All',
            area: {
                area_id: '',
                area_name: 'All'
            },
            location_status: {value: 0, key: "live"},
            map_lat: 0,
            map_long: 0
        });

        $scope.location_id = $scope.locations[0].location_id;

        $scope.controlled_substances = controlledSubstances.results;

        $scope.controlled_substance = {};

        $scope.list = {
            items: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'controlled_substance__controlled_substance_name',
            loading: false,
            selected: 0,
            dateFrom: moment(diff).format('YYYY-MM-DD'),
            dateTo: moment(current).format('YYYY-MM-DD'),

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

                growl.info("LOADING_STOCK");

                var start_time = toUTC(moment($scope.list.dateFrom).format('YYYY-MM-DD 00:00:00'));
                var end_time = toUTC(moment($scope.list.dateTo).format('YYYY-MM-DD 23:59:59'));

                StockService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, '', $scope.list.predicate, $scope.list.reverse, $scope.current_status, $scope.location_id, $scope.controlled_substance.controlled_substance_id, start_time, end_time)
                    .then(function (data) {
                        $scope.list.items = data.results;
                        $scope.list.summary = data.summary;
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);

                        $scope.list.selected = 0;

                        $scope.chart = {
                            type: 'PieChart',
                            data: {
                                "cols": [
                                    {id: "name", label: "", type: "string"},
                                    {id: "count", label: "Count", type: "number"}
                                ],
                                "rows": [
                                    {
                                        c: [
                                            {v: $translate.instant('in_stock')},
                                            {v: data.summary.in}
                                        ]
                                    },
                                    {
                                        c: [
                                            {v: $translate.instant('allocated')},
                                            {v: data.summary.out}
                                        ]
                                    }
                                ]
                            },

                            options: {
//              "title": "Incidents",
//              "fill": 20,
                                pieHole: 1,
                                legend: {position: 'none'},
                                chartArea: {
                                    left: 0,
                                    top: 10,
                                    width: '100%',
                                    height: '150'
                                },
                                "displayExactValues": true,
                                //"vAxis": {
                                //    "title": "Incidents", "gridlines": {"count": 6}
                                //},
//                                focusTarget: 'category',
                                tooltip: {isHtml: true},
                                //"hAxis": {
                                //    "title": $scope.scale.value
                                //},
                                "colors": [
                                    '#35bfbf',
                                    '#fd423e',
                                    '#ffb648',
                                    '#949fb3',
                                    '#4c5261'
                                ]
                            },

                            formatters: {}
                        };
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

                growl.info("LOADING_STOCK");

                StockService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, text, $scope.list.predicate, $scope.list.reverse)
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

            archive: function (controlled_substance_id) {
                console.log("removing");

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/controlled_substances/templates/confirm.html',
                    controller: 'ConfirmModalCtrl',
                    size: 'md'
                });

                modalInstance.result.then(function () {
                    StockService.remove(controlled_substance_id).then(function (response) {
                        $scope.list.get();
                    }, function (error) {
                        growl.error(error.detail);
                    });

                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                });
            },

            //checkout: function (data) {
            //
            //},

            check_in: function (data) {
                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/stocks/templates/checkin.html',
                    controller: 'StockCheckinCtrl',
                    size: 'md',
                    resolve: {
                        data: function () {
                            return data;
                        },
                        controlledSubstances: function () {
                            return controlledSubstances;
                        },
                        locations: function () {
                            return locations;
                        }

                    }
                });

                modalInstance.result.then(function () {
                        $timeout(function () {
                            $scope.list.get();
                        }, 100);
                    }, function () {
                        $log.info('Modal dismissed at: ' + new Date());
                    }
                );
            },

            dispose: function () {
                var data = angular.copy($scope.list.items);

                var selected = _.filter(data, function (item) {
                    return item.hasOwnProperty('selected') && item.selected;
                });

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/stocks/templates/dispose.html',
                    controller: 'StockDisposeCtrl',
                    keyboard: false,
                    size: 'md',
                    resolve: {
                        data: function () {
                            return selected;
                        },
                        controlledSubstances: function () {
                            return controlledSubstances;
                        },
                        locations: function () {
                            return locations;
                        }

                    }
                });

                modalInstance.result.then(function () {
                    $timeout(function () {
                        $scope.list.get();
                    }, 100);
                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                }).finally(function () {

                });
            },

            relocate: function () {
                var data = angular.copy($scope.list.items);

                var selected = _.filter(data, function (item) {
                    return item.hasOwnProperty('selected') && item.selected;
                });

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: '/app/stocks/templates/relocate.html',
                    controller: 'StockRelocateCtrl',
                    keyboard: false,
                    size: 'md',
                    resolve: {
                        data: function () {
                            return selected;
                        },
                        controlledSubstances: function () {
                            return controlledSubstances;
                        },
                        locations: function () {
                            return locations;
                        }
                    }
                });

                modalInstance.result.then(function () {
                    $timeout(function () {
                        $scope.list.get();
                    }, 100);

                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                }).finally(function () {

                });
            }
        };

        $scope.selection_update = function (value) {
            if (value) {
                $scope.list.selected++;
            } else {
                $scope.list.selected--;
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

        $scope.$watch(
            'current_status',
            function (newValue, oldValue) {
                if (newValue && newValue !== oldValue) {
                    $scope.current_status_text = statuses[$scope.current_status];
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);


                }
            }
        );

        $scope.$watch(
            'controlled_substance.controlled_substance_id',
            function (newValue, oldValue) {
                if (newValue && newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        $scope.$watch(
            'location_id',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        //$scope.$watch(
        //    'bulk_action',
        //    function (newValue, oldValue) {
        //        if (newValue) {
        //
        //            if (newValue == 'dispose') {
        //                $scope.list.dispose();
        //            }
        //
        //            if (newValue == 'relocate') {
        //                $scope.list.relocate();
        //            }
        //        }
        //    }
        //);

        $scope.bulk_selection_update = function (newValue) {
            if (newValue == 'dispose') {
                $scope.list.dispose();
            }

            if (newValue == 'relocate') {
                $scope.list.relocate();
            }
        };


        var filterTextTimeout;

        $scope.$watch(
            'search',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {

                    if (filterTextTimeout) {
                        $timeout.cancel(filterTextTimeout);
                    }

                    filterTextTimeout = $timeout(function () {
                        //console.log("value changed");
                        $scope.list.search(newValue);
                    }, 1000); // delay 250 ms


                }
            }
        );
    }]);
