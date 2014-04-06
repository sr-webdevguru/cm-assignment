'use strict';
angular.module('app')
    .controller('DashboardCtrl', function ($scope, $rootScope, $state, $timeout, $log, $intercom, AnalyticsService, QuestionService, growl, DateRangeService, currentUser, $translate) {

        function checkNested(obj /*, level1, level2, ... levelN*/) {
            var args = Array.prototype.slice.call(arguments, 1);

            for (var i = 0; i < args.length; i++) {
                if (!obj || !obj.hasOwnProperty(args[i])) {
                    return false;
                }
                obj = obj[args[i]];
            }

            return true;
        }

        function arrayToObj(array) {
            var map = {};
            var values = $.map(array, function (val, i) {
                for (var key in val) {
                    map[key] = val[key];
                }
            });
            map[""] = $translate.instant("Unknown");
            map["Unknown"] = $translate.instant("Unknown");
            return map;
        }

        $intercom.update({
            email: currentUser.email,
            name: currentUser.name,
            created_at: new Date(),
            user_id: currentUser.user_id,
            company: {
                id: currentUser.resorts[0].resort_id,
                name: currentUser.resorts[0].resort_name
            },
            role: currentUser.role_id[0].key,
            dashboard_feature_last_used: "Dashboard"
        });

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        var date_format = $scope.datetime_format.slice(0,10);
        $scope.date_format = date_format_mapping[date_format];

        var resort_id = currentUser.resorts[0].resort_id;

        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        var timer = null;

        $scope.list = DateRangeService.range;

        $scope.init = function () {

            growl.info('SYNCING_DATA');

            QuestionService.fetch().then(function (questions) {

                var start_time = moment($scope.list.dateFrom).format('YYYY-MM-DD hh:mm:ss');
                var end_time = moment($scope.list.dateTo).format('YYYY-MM-DD hh:mm:ss');

                AnalyticsService.fetchSex(start_time, end_time, resort_id).then(function (result) {

                    var rows = result.data.map(function (item) {
                        return {
                            c: [
                                {v: months[item.month - 1] + ', ' + item.year},
                                {v: item.male},
                                {v: item.female},
                                {v: item.unknown}
                            ]
                        }
                    });

                    $scope.by_incidents = {
                        type: "LineChart",
                        data: {
                            "cols": [
                                {id: "month", label: "Month", type: "string"},
                                {id: "incidents-num-1", label: "Male", type: "number"},
                                {id: "incidents-num-2", label: "Female", type: "number"},
                                {id: "incidents-num-3", label: "Unknown", type: "number"}
                            ], "rows": rows
                        },

                        options: {
//                "title": "Incidents",
//                "fill": 20,
                            "displayExactValues": true,
                            "vAxis": {
                                "title": "Incidents", "gridlines": {"count": 6}
                            },
//                "hAxis": {
//                    "title": "Date"
//                },
                            "colors": [
                                '#35bfbf',
                                '#ffb547',
                                '#4c5261'
                            ]
                        },

                        formatters: {}
                    };
                });

                AnalyticsService.fetchActivity(start_time, end_time, resort_id).then(function (result) {

                    if (checkNested(questions, 'DashboardItems', 'field_52ca41790a16c', 'Questions', 'field_52ca3dc8ac437', 'Values')) {
                        var map = arrayToObj(questions.DashboardItems.field_52ca41790a16c.Questions.field_52ca3dc8ac437.Values);


                        var rows = result.data.map(function (item) {
                            return {
                                c: [
                                    {v: $translate.instant(map[item.activity])},
                                    {v: parseFloat(item.percent)}
                                ]
                            }
                        });

                        $scope.by_activities = {
                            type: "PieChart",
                            cssStyle: "height:450px; width:300px;background-color:transparent;",
                            data: {
                                "cols": [
                                    {id: "activity", label: "Activity", type: "string"},
                                    {id: "num", label: "Events", type: "number"}
                                ],
                                "rows": rows
                            },

                            options: {
//                "title": "Incidents",
                                pieHole: 0.5,
//                "fill": 20,
                                "displayExactValues": true,
                                "vAxis": {
                                    "title": "No. of Incidents", "gridlines": {"count": 6}
                                },
                                "hAxis": {
                                    "title": "Date"
                                },
                                "colors": [
                                    '#fd423e',
                                    '#35bfbf',
                                    '#ffb648',
                                    '#949fb3',
                                    '#4c5261'
                                ]
                            },

                            formatters: {}
                        };
                    }
                });

                AnalyticsService.fetchPatrollers(start_time, end_time).then(function (result) {
                    $scope.patrollers = result.data;
                });

                AnalyticsService.fetchInjury(start_time, end_time, resort_id).then(function (result) {

                    if (checkNested(questions, 'DashboardItems', 'field_52d4798f6d229', 'Questions', 'field_52d4798f6d227', 'RepeatingQuestions', 'injury_type', 'Values')) {
                        var map = arrayToObj(questions.DashboardItems.field_52d4798f6d229.Questions.field_52d4798f6d227.RepeatingQuestions.injury_type.Values);

                        var rows = result.data.map(function (item) {
                            return {
                                c: [
                                    {v: $translate.instant(map[(item.injury).replace(/"/g, '')]) },
                                    {v: item.num}
                                ]
                            }
                        });

                        $scope.by_injury_types = {
                            type: "ColumnChart",
                            cssStyle: "height:450px; width:300px;background-color:transparent;",
                            data: {
                                "cols": [
                                    {id: "injury", label: "Injury", type: "string"},
                                    {id: "num", label: "Injury", type: "number"}
//                        {role: "style", type: "string"}
                                ], "rows": rows
                            },

                            options: {
//                "title": "Incidents",
//                "fill": 20,
                                "displayExactValues": true,
                                "vAxis": {
                                    "title": "Count", "gridlines": {"count": 6}
                                },
//                "hAxis": {
//                    "title": "Date"
//                },
                                "colors": [
                                    '#fd423e',
                                    '#35bfbf',
                                    '#ffb648',
                                    '#949fb3',
                                    '#4c5261'
                                ]
                            },

                            formatters: {}
                        };
                    }
                });

                AnalyticsService.fetchReferred(start_time, end_time, resort_id).then(function (result) {

                    if (checkNested(questions, 'DashboardItems', 'field_52ca426c0a178', 'Questions', 'field_52d48077a16be', 'Values')) {
                        var map = arrayToObj(questions.DashboardItems.field_52ca426c0a178.Questions.field_52d48077a16be.Values);

                        var rows = result.data.map(function (item) {
                            return {
                                c: [
                                    {v: $translate.instant(map[item.referred_to])},
                                    {v: parseFloat(item.percent)}
                                ]
                            }
                        });

                        $scope.by_referred = {
                            type: "PieChart",
                            cssStyle: "height:400px; width:300px;background-color:transparent;",
                            data: {
                                "cols": [
                                    {id: "month", label: "Month", type: "string"},
                                    {id: "incidents-num-1", label: "Party1", type: "number"}
                                ], "rows": rows
                            },

                            options: {
//                "title": "Incidents",
                                pieHole: 0.5,
//                "fill": 20,
                                "displayExactValues": true,
                                "vAxis": {
                                    "title": "No. of Incidents", "gridlines": {"count": 6}
                                },
                                "hAxis": {
                                    "title": "Date"
                                },
                                "colors": [
                                    '#fd423e',
                                    '#35bfbf',
                                    '#ffb648',
                                    '#949fb3',
                                    '#4c5261'
                                ]
                            },

                            formatters: {}
                        };
                    }
                });

                AnalyticsService.fetchAge(start_time, end_time, resort_id).then(function (result) {
                    var data = result.data;
                    $scope.by_age = {
                        type: "ColumnChart",
                        cssStyle: "height:400px; width:300px;background-color:transparent;",
                        data: {
                            "cols": [
                                {id: "month", label: "Month", type: "string"},
                                {id: "incidents-num-1", label: "Age", type: "number"},
                                {role: "style", type: "string"}
                            ], "rows": [
                                {
                                    c: [
                                        {v: "0-10"},
                                        {v: data.g0_10},
                                        {v: '#fd423e'}
                                    ]
                                },
                                {
                                    c: [
                                        {v: "11-15"},
                                        {v: data.g11_15},
                                        {v: '#35bfbf'}
                                    ]
                                },
                                {
                                    c: [
                                        {v: "16-18"},
                                        {v: data.g16_18},
                                        {v: '#ffb648'}
                                    ]
                                },
                                {
                                    c: [
                                        {v: "19-21"},
                                        {v: data.g19_21},
                                        {v: '#949fb3'}
                                    ]
                                },
                                {
                                    c: [
                                        {v: "22-30"},
                                        {v: data.g22_30},
                                        {v: '#4c5261'}
                                    ]
                                },
                                {
                                    c: [
                                        {v: "31-"},
                                        {v: data.g31_},
                                        {v: '#000000'}
                                    ]
                                }
                            ]
                        },

                        options: {
//                "title": "Incidents",
//                "fill": 20,
                            "displayExactValues": true,
                            "vAxis": {
                                "title": "Count", "gridlines": {"count": 6}
                            },
//                "hAxis": {
//                    "title": "Date"
//                },
                            "colors": [
                                '#fd423e',
                                '#35bfbf',
                                '#ffb648',
                                '#949fb3',
                                '#4c5261',
                                '#000000'
                            ]
                        },

                        formatters: {}
                    };
                });

                AnalyticsService.fetchAlcohol(start_time, end_time, resort_id).then(function (result) {
                    var rows = result.data.map(function (item) {
                        return {
                            c: [
                                {v: months[item.month] + ', ' + item.year},
                                {v: item.alcohol},
                                {v: item.drugs}
                            ]
                        }
                    });

                    $scope.by_drugs = {
                        type: "ColumnChart",
                        cssStyle: "height:400px; width:300px;background-color:transparent;",
                        data: {
                            "cols": [
                                {id: "month", label: "Month", type: "string"},
                                {id: "count-alcohol", label: "Alcohol", type: "number"},
                                {id: "count-drugs", label: "Drugs", type: "number"}
                            ], "rows": rows
                        },

                        options: {
//                "title": "Incidents",
//                "fill": 20,
                            "displayExactValues": true,
                            "vAxis": {
                                "title": "Count", "gridlines": {"count": 6}
                            },
//                "hAxis": {
//                    "title": "Date"
//                },
                            "colors": [
                                '#fd423e',
                                '#35bfbf',
                                '#ffb648',
                                '#949fb3',
                                '#4c5261'
                            ]
                        }
                    };
                });


//            timer = $timeout($scope.init, 15000);
//
//            $scope.$on(
//                "$destroy",
//                function( event ) {
//
//                    $timeout.cancel( timer );
//
//                }
//            );

            }, function (reason) {
                $rootScope.on_error(reason);
            });


        };

        $scope.css = "height:270px;background-color:transparent;";

    });