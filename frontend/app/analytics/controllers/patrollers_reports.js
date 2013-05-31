/**
 * Created by rj on 13/9/16.
 */

'use strict';
angular.module('app')
    .controller('PatrollersReportCtrl', ['$scope', '$log', 'currentUser', 'growl', '$window', '$translate', 'ReportService',
        function ($scope, $log, currentUser, growl, $window, $translate, ReportService) {
        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        var date_format = $scope.datetime_format.slice(0,10);
        $scope.date_format = date_format_mapping[date_format];
        console.log($scope.date_format)
        $scope.css = "height:175px;background-color:transparent;";
        $scope.properties = {
            date_range:{
                select: {
                    options: [
                        { id: 0, text: $translate.instant('last_seven_days'), value: 'LAST_7_DAYS' },
                        { id: 1, text: $translate.instant('last_thirty_days'), value: 'LAST_30_DAYS' },
                        { id: 2, text: $translate.instant('last_six_months'), value: 'LAST_6_MONTHS' },
                        { id: 3, text: $translate.instant('last_twelve_months'), value: 'LAST_12_MONTHS' },
                        { id: 4, text: $translate.instant('custom_date_range'), value: 'CUSTOM' }
                    ],
                    model_value: { id: 0, text: $translate.instant('last_seven_days'), value: 'LAST_7_DAYS' },
                    onChange: function(text_range){
                        var from = moment();
                        var to = moment();
                        switch(text_range.value){
                            case 'LAST_7_DAYS': { from.subtract(7, 'days'); break; }
                            case 'LAST_30_DAYS': { from.subtract(30, 'days'); break; }
                            case 'LAST_6_MONTHS': { from.subtract(6, 'months'); break; }
                            case 'LAST_12_MONTHS': {from.subtract(12, 'months'); break; }
                            default: {
                                from = moment($scope.properties.date_range.from, false);
                                break;
                            }
                        }
                        $scope.properties.date_range.from = from.format();
                        $scope.properties.date_range.to = to.format();
                    }
                },
                format: date_format,
                from: moment().subtract(7, 'days').format(),
                to: moment().format(),
                pickers: {
                    frontHandled: false,
                    onChange: function(value){
                        $scope.properties.date_range.pickers.frontHandled = value == 'frontHandled';
                    }
                }
            }
        };
        $scope.report = {
            params : {
                output_format: 'json',
                datefrom: moment().subtract(7, 'days').utc().format('YYYY-MM-DD+00:00:00'),
                dateto: moment().utc().format('YYYY-MM-DD+23:59:59')
            }
        };

        $scope.$watch('properties.date_range.from', function(newValue, oldValue){
            if ($scope.properties && $scope.properties.date_range.pickers.frontHandled) {
                $scope.properties.date_range.select.model_value =
                    $scope.properties.date_range.select.options[($scope.properties.date_range.select.options.length - 1)];
                $scope.properties.date_range.pickers.frontHandled = false;
            }
            if (newValue !== oldValue){
                $scope.report.params.datefrom = moment(newValue).utc().format('YYYY-MM-DD+00:00:00');
                $scope.list.get();
            }
        });
        $scope.$watch('properties.date_range.to', function(newValue, oldValue){
            if ($scope.properties && $scope.properties.date_range.pickers.frontHandled) {
                $scope.properties.date_range.select.model_value =
                    $scope.properties.date_range.select.options[($scope.properties.date_range.select.options.length - 1)];
                $scope.properties.date_range.pickers.frontHandled = false;
            }
            if (newValue !== oldValue){
                $scope.report.params.dateto = moment(newValue).utc().format('YYYY-MM-DD+23:59:59');
                $scope.list.get();
            }
        });


        $scope.list = {
            items: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'name',
            loading: false,
            reverse: false,

            setPage: function (pageNum) {
                $scope.list.currentPage = pageNum;
            },

            sortBy: function (predicate) {
                $scope.list.predicate = predicate;
                $scope.list.reverse = !$scope.list.reverse;
                $scope.list.get();
            },

            get: function () {
                $log.log('fetching items...');
                $scope.list.loading = true;

                growl.info("LOADING_PATROLLERS_REPORT");
                $scope.report.params.output_format = 'json';
                $scope.report.params.offset = ($scope.list.currentPage - 1) * $scope.list.itemsPerPage;
                $scope.report.params.chunk = $scope.list.itemsPerPage;
                $scope.report.params.order_by = $scope.list.predicate;
                $scope.report.params.order_by_direction = $scope.list.reverse? 'desc' : 'asc';
                ReportService.fetchPatrollers($scope.report.params)
                    .then(function(response){
                        console.log(response);
                        $scope.list.items = response.data;
                        $scope.list.totalItems = response.total_rows;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);

                    }, function(error){
                        growl.error(error.detail);
                    })
                    .finally(function () {
                        $scope.list.loading = false;
                    });
            },
            download: function(){
                growl.info("DOWNLOADING_PATROLLERS_REPORT");
                ReportService.fetchPatrollers({
                    datefrom: $scope.report.params.datefrom,
                    dateto: $scope.report.params.dateto,
                    output_format: 'csv'
                })
                    .then(function(data){
                        var anchor = angular.element('<a/>');
                        anchor.attr({
                            href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                            target: '_blank',
                            download: 'patrollers_report.csv'
                        })[0].click();
                    }, function(error){
                        growl.error(error.detail);
                    })
                    .finally(function () {
                        $scope.list.loading = false;
                    });
            },
            print: function(){
                $window.print();
            }
        };

        $scope.$watch(
            'list.itemsPerPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                }
            }
        );

        $scope.$watch(
            'list.currentPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                }
            }
        );
        $scope.$on('$viewContentLoaded', function(){
            $scope.list.get();
        });
    }]);