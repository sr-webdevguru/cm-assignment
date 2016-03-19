'use strict';

angular.module('app')
    .controller('ReportCtrl', function ($scope, $location, $state, $stateParams, $rootScope, $timeout, $log, $q, $window, $intercom, $translate, IncidentService, DateRangeService, ReportService, questions, currentUser, growl) {

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
            dashboard_feature_last_used: "Reports"
        });

        var current = new Date();
        var tz = jstz.determine();

        var resort = currentUser.resorts[0];
        var resort_id = resort.resort_id;

        function toUTC(value) {
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format('YYYY-MM-DD HH:mm:ss');
        }

        $scope.id = $stateParams.reportId;

        $scope.schema = {
            type: "object",
            properties: []
        };

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        var date_format = $scope.datetime_format.slice(0,10);
        $scope.date_format = date_format_mapping[date_format];


//        Schema	Form type
//        "type": "string"	text
//        "type": "number"	number
//        "type": "integer"	number
//        "type": "boolean"	checkbox
//        "type": "object"	fieldset
//        "type": "string" and a "enum"	select
//        "type": "array" and a "enum" in array type	checkboxes
//        "type": "array"	array

        var schema_type = {
            'text': 'string',
            'textarea': 'string',
            'number': 'string',
            'range': 'string',
            'arrows': 'string',
            'select': 'string',
            'multi_select': 'string',
            'radio': 'string',
            'radio_button': 'string',
            'gender': 'string',
            'image': 'object',
            'date_picker': 'string',
            'date_time_picker': 'string',
            'google_map': 'object',
            'file': 'string'
        };

//        Form Type	Becomes
//        fieldset	a fieldset with legend
//        section	just a div
//        conditional	a section with a ng-if
//        actions	horizontal button list, can only submit and buttons as items
//        text	input with type text
//        textarea	a textarea
//        number	input type number
//        password	input type password
//        checkbox	a checkbox
//        checkboxes	list of checkboxes
//        select	a select (single value)
//        submit	a submit button
//        button	a button
//        radios	radio buttons
//        radios-inline	radio buttons in one line
//        radiobuttons	radio buttons with bootstrap buttons
//        help	insert arbitrary html
//        tab	tabs with content
//        array	a list you can add, remove and reorder
//        tabarray	a tabbed version of array

        var form_type = {
            'text': 'text',
            'range': 'text',
            'textarea': 'text',
            'number': 'number',
            'arrows': 'select',
            'select': 'select',
            'multi_select': 'select',
            'radio': 'select',
            'radio_button': 'select',
            'gender': 'select',
            'image': 'file_upload',
            'message': 'help',
            'date_picker': 'date_picker',
            'date_time_picker': 'date_time_picker',
            'google_map': 'googlemap',
            'file': 'text'
        };

        var chosenTypes = [
            'text',
            'range',
            'textarea',
            'number',
            'decimal',
            'arrows',
            'select',
            'multi_select',
            'radio',
            'radio_button',
            'gender',
            'date_picker',
            'date_time_picker'
        ];

        var tabs = questions.DashboardItems;

        var getChoiceMap = function (mapValues) {
            var _choices = [],
                _titlemap = [];

            // Loop and build choices and titlemap
            angular.forEach(mapValues, function (value) {
                for (var key in value) {
                    if (key.indexOf("controlled") < 0) {
                        _choices.push({"id": key, "name": $translate.instant(value[key])});
                        _titlemap.push({"value": key, "name": $translate.instant(value[key])});
                    }
                }
            });

            return {
                "choices": _choices,
                "titlemap": _titlemap
            }
        };

        for (var key in tabs) {
            if (tabs.hasOwnProperty(key)) {


                for (var question in tabs[key]) {
                    if (tabs[key].hasOwnProperty(question) && (question == 'Questions' || question == 'RepeatingQuestions')) {
                        var temp_schema_properties_question = [];

                        for (var m in tabs[key][question]) {
                            if (tabs[key][question].hasOwnProperty(m)) {


                                var q = tabs[key][question][m];

                                var choices = [];
                                var titlemap = [];

                                if (q.Type == 'select' || q.Type == 'multi_select' || q.Type == 'arrows') {

                                    for (var key1 in q.Values) {

                                        if (q.Values.hasOwnProperty(key1)) {

                                            var choiceMap = getChoiceMap(q.Values);

                                            choices = choiceMap.choices;
                                            titlemap = choiceMap.titlemap;

                                        }

                                    }
                                }

                                if (q.Type == 'gender') {
                                    titlemap.push({
                                        value: "Male",
                                        name: "Male"
                                    });

                                    titlemap.push({
                                        value: "Female",
                                        name: "Female"
                                    });
                                }

                                if (q.Type == 'radio') {
                                    titlemap.push({
                                        value: "Yes",
                                        name: "Yes"
                                    });

                                    titlemap.push({
                                        value: "No",
                                        name: "No"
                                    });
                                }

                                if (q.Type == 'radio_button') {
                                    titlemap.push({
                                        value: "yes",
                                        name: "Yes"
                                    });

                                    titlemap.push({
                                        value: "no",
                                        name: "No"
                                    });

                                    titlemap.push({
                                        value: "unknown",
                                        name: "Unknown"
                                    });
                                }

                                if (chosenTypes.indexOf(q.Type) > -1) {
                                    if(!q.hasOwnProperty('ParentKey') || (q.hasOwnProperty('ParentKey') && tabs[key][question].hasOwnProperty(q['ParentKey']))) {
                                        if(q.hasOwnProperty('ParentKey')){
                                            temp_schema_properties_question.forEach(function(current, index, array){
                                                if(current.key == q['ParentKey']){
                                                    var fullkey = m;

                                                    if (question == 'RepeatingQuestions') {
                                                        fullkey = key + '____' + m;
                                                    }

                                                    if(current.hasOwnProperty('childField')){
                                                        titlemap.unshift({
                                                            value: "all",
                                                            name: "All"
                                                        });
                                                        temp_schema_properties_question[index]['childField'][q['ShowIf'][q['ParentKey']]] = {
                                                            'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                                            'order': q.Order,
                                                            'fullkey': fullkey,
                                                            'key': m,
                                                            'placeholder': $translate.instant(q.Placeholder),
                                                            'titleMap': titlemap
                                                        };
                                                        temp_schema_properties_question[index]['childField'][q['ShowIf'][q['ParentKey']]]['select'] = [
                                                            {
                                                                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                                                'fullkey': fullkey
                                                            }
                                                        ]
                                                    }
                                                    else{
                                                        var selection_name = q['ShowIf'][q['ParentKey']];
                                                        temp_schema_properties_question[index]['childField'] = {};
                                                        titlemap.unshift({
                                                            value: "all",
                                                            name: "All"
                                                        });
                                                        temp_schema_properties_question[index]['childField'][selection_name] = {
                                                            'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                                            'order': q.Order,
                                                            'fullkey': fullkey,
                                                            'key': m,
                                                            'placeholder': $translate.instant(q.Placeholder),
                                                            'titleMap': titlemap
                                                        };
                                                        temp_schema_properties_question[index]['childField'][selection_name]['select'] = [
                                                            {
                                                                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                                                'fullkey': fullkey
                                                            }
                                                        ];
                                                    }
                                                }
                                            })
                                        }
                                        else{
                                            var fullkey = m;

                                            if (question == 'RepeatingQuestions') {
                                                fullkey = key + '____' + m;
                                            }

                                            temp_schema_properties_question.push({
                                                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                                'type': schema_type[q.Type],
                                                'order': q.Order,
                                                'fullkey': fullkey,
                                                'key': m,
                                                'formtype': form_type[q.Type],
                                                'placeholder': $translate.instant(q.Placeholder),
                                                'titleMap': titlemap
                                            });
                                        }
                                    }
                                } else {
                                    if (q.Type == "repeater" && q.hasOwnProperty('RepeatingQuestions')) {
                                        for (var question1 in tabs[key][question][m]) {
                                            if (tabs[key][question][m].hasOwnProperty(question1) && (question1 == 'Questions' || question1 == 'RepeatingQuestions')) {
                                                var temp_schema_properties = [];
                                                for (var n in tabs[key][question][m][question1]) {
                                                    if (tabs[key][question][m][question1].hasOwnProperty(n)) {
                                                        var q1 = tabs[key][question][m][question1][n];

                                                        var choices = [];
                                                        var titlemap = [];

                                                        if (q1.Type == 'select' || q1.Type == 'multi_select' || q1.Type == 'arrows') {

                                                            for (var key11 in q1.Values) {

                                                                if (q1.Values.hasOwnProperty(key11)) {

                                                                    var choiceMap = getChoiceMap(q1.Values);

                                                                    choices = choiceMap.choices;
                                                                    titlemap = choiceMap.titlemap;

                                                                }
                                                            }
                                                        }

                                                        if (q1.Type == 'gender') {
                                                            titlemap.push({
                                                                value: "Male",
                                                                name: "Male"
                                                            });

                                                            titlemap.push({
                                                                value: "Female",
                                                                name: "Female"
                                                            });
                                                        }

                                                        if (q1.Type == 'radio') {
                                                            titlemap.push({
                                                                value: "Yes",
                                                                name: "Yes"
                                                            });

                                                            titlemap.push({
                                                                value: "No",
                                                                name: "No"
                                                            });
                                                        }


                                                        if (q.Type == 'radio_button') {
                                                            titlemap.push({
                                                                value: "yes",
                                                                name: "Yes"
                                                            });
                                                            titlemap.push({
                                                                value: "no",
                                                                name: "No"
                                                            });

                                                            titlemap.push({
                                                                value: "unknown",
                                                                name: "Unknown"
                                                            });
                                                        }

                                                        if (!q1.hasOwnProperty('ParentKey') || (q1.hasOwnProperty('ParentKey') && tabs[key][question][m][question1].hasOwnProperty(q1['ParentKey']))) {
                                                            if (q1.hasOwnProperty('ParentKey')) {
                                                                if (chosenTypes.indexOf(q1.Type) > -1) {
                                                                    temp_schema_properties.forEach(function (current, index, array) {
                                                                        if (current.key == q['ParentKey']) {
                                                                            if (current.hasOwnProperty('childField')) {
                                                                                titlemap.unshift({
                                                                                    value: "all",
                                                                                    name: "All"
                                                                                });
                                                                                temp_schema_properties[index]['childField'][q['ShowIf'][q['ParentKey']]] = {
                                                                                    'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                                    'fullkey': m + '____' + n,
                                                                                    'key': n,
                                                                                    'placeholder': $translate.instant(q1.Placeholder),
                                                                                    'titleMap': titlemap
                                                                                };
                                                                                temp_schema_properties[index]['childField'][q1['ShowIf'][q1['ParentKey']]]['select'] = [
                                                                                    {
                                                                                        'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                                        'fullkey': fullkey
                                                                                    }
                                                                                ]
                                                                            }
                                                                            else {
                                                                                var selection_name = q1['ShowIf'][q1['ParentKey']];
                                                                                temp_schema_properties[index]['childField'] = {};
                                                                                titlemap.unshift({
                                                                                    value: "all",
                                                                                    name: "All"
                                                                                });
                                                                                temp_schema_properties[index]['childField'][selection_name] = {
                                                                                    'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                                    'fullkey': m + '____' + n,
                                                                                    'key': n,
                                                                                    'placeholder': $translate.instant(q1.Placeholder),
                                                                                    'titleMap': titlemap
                                                                                };
                                                                                temp_schema_properties[index]['childField'][selection_name]['select'] = [
                                                                                    {
                                                                                        'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                                        'fullkey': fullkey
                                                                                    }
                                                                                ]

                                                                            }
                                                                        }
                                                                    })
                                                                }
                                                            }
                                                            else {
                                                                if (chosenTypes.indexOf(q1.Type) > -1) {
                                                                    temp_schema_properties.push({
                                                                        'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                        'type': schema_type[q1.Type],
                                                                        'order': q1.Order,
                                                                        'fullkey': m + '____' + n ,
                                                                        'key': n,
                                                                        'formtype': form_type[q1.Type],
                                                                        'placeholder': $translate.instant(q1.Placeholder),
                                                                        'titleMap': titlemap
                                                                    });
                                                                }
                                                            }


                                                            //if(!q1.hasOwnProperty('ParentKey') || (q1.hasOwnProperty('ParentKey') && tabs[key][question][m][question1].hasOwnProperty(q1['ParentKey']))) {
                                                            //    if(q1.hasOwnProperty('ParentKey')){
                                                            //        if (chosenTypes.indexOf(q1.Type) > -1) {
                                                            //        }
                                                            //    }
                                                            //    else{
                                                            //        if (chosenTypes.indexOf(q1.Type) > -1) {
                                                            //            temp_schema_properties.push({
                                                            //                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                            //                'type': schema_type[q1.Type],
                                                            //                'order': q1.Order,
                                                            //                'fullkey': m + '____' + n,
                                                            //                'key': n,
                                                            //                'formtype': form_type[q1.Type],
                                                            //                'placeholder': $translate.instant(q1.Placeholder),
                                                            //                'titleMap': titlemap
                                                            //            });
                                                            //        }
                                                            //    }
                                                            //}
                                                        }
                                                    }
                                                }
                                                $scope.schema.properties = $scope.schema.properties.concat(temp_schema_properties);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        $scope.schema.properties = $scope.schema.properties.concat(temp_schema_properties_question);
                    }
                }
            }
        }

        $scope.model = {
            filters: [
                {}
            ]
        };

        $scope.onSubmit = function (form) {
            $log.log($scope.model);

            $scope.list.get();
        };

        $scope.onReset = function () {
            $scope.model.filters = [
                {}
            ];
        };

        $scope.onDownload = function (form) {
            var start_time = toUTC(moment($scope.list.range.dateFrom).format('YYYY-MM-DD 00:00:00'));
            var end_time = toUTC(moment($scope.list.range.dateTo).format('YYYY-MM-DD 23:59:59'));
            IncidentService.fetchReport(start_time, end_time, $scope.list.itemsPerPage, $scope.list.currentPage, $scope.model.filters, resort_id, 'csv').then(
                function (data) {
                    $log.log(data);

                    var anchor = angular.element('<a/>');
                    anchor.attr({
                        href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                        target: '_blank',
                        download: 'report.csv'
                    })[0].click();
                }
            );

        };

//        function lazyLoadExportData() {
//            var deferred = $q.defer();
//
//            IncidentService.fetchReport($scope.model.dateFrom, $scope.model.dateTo, tz.name(), $scope.model)
//                .then(function (data) {
//                    $log.log(data);
//
//                    deferred.resolve(
//                        data.map(function (incident) {
//                            return {
//                                id: incident.id,
//                                datetime: incident.datetime,
//                                casualty: incident.casualty,
//                                injury: incident.injury,
//                                type: incident.type,
//                                activity: incident.activity,
//                                status: incident.status
//                            };
//                        })
//                    );
//
//                }, function (errorData) {
//                    deferred.reject(errorData);
//                });
//
//
//            return deferred.promise;
//        }


        $scope.addField = function (filters) {
            filters.push({});
        };

        $scope.removeField = function (index) {
            $scope.model.filters.splice(index, 1);
        };

        $scope.list = {
            range: DateRangeService.range,
            incidents: [],
            currentPage: 1,
            itemsPerPage: 20,
            filteredItems: 0,
            totalItems: 0,
            totalPages: 0,
            predicate: 'dt_created',
            loading: false,
            success: true,
            error: '',

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
            },

            get: function () {
                $log.log('fetching incidents...');
                $scope.list.loading = true;

                var start_time = toUTC(moment($scope.list.range.dateFrom).format('YYYY-MM-DD 00:00:00'));
                var end_time = toUTC(moment($scope.list.range.dateTo).format('YYYY-MM-DD 23:59:59'));

                IncidentService.fetchReport(start_time, end_time, $scope.list.itemsPerPage, $scope.list.currentPage, $scope.model.filters, resort_id, 'json').then(
                    function (data) {
                        $log.log(data);

                        $scope.list.loading = false;

                        angular.forEach(data.results, function(elem, index) {
                            data.results[index]['dt_created'] = moment(elem['dt_created'], 'YYYY-MM-DD HH:mm:ss').format($scope.datetime_format);
                        });

                        $scope.list.incidents = data.results;
                        $scope.list.filteredItems = ($scope.list.incidents == null) ? 0 : $scope.list.incidents.length; //Initially for no filter
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                        $scope.list.sort_by('dt_created');
                        $scope.list.reverse = true;

                    }, function (reason) {
                        growl.error(reason.detail);

                        $scope.list.incidents = [];
                        $scope.list.success = false;
                        $scope.list.error = reason.detail;
                        $scope.list.loading = false;
                    });
            },

            print: function (id) {
                $log.log('printing incident ' + id);

                if (id !== null || id !== undefined) {
                    IncidentService.print(id)
                        .then(function (data) {
//                            $log.log(data.data.URL);
                            $window.open(data.data.URL, '_blank', '');

                        }, function (error) {
                            $scope.error = error;
                        });
                }

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

        $scope.report = {
            label: "",
            global: 0,
            config: {
                url: {},
                body: {}
            }
        };

        $scope.getReport = function (id) {
            ReportService.fetch(id).then(function (data) {
                $log.log(data);

                growl.success("report_fetched_successfully");

                $scope.report = data;
                $scope.report.global = $scope.report.global > 0;
                $scope.list.range.dateFrom = toLocalTime($scope.report.config.url.datefrom);
                $scope.list.range.dateTo = toLocalTime($scope.report.config.url.dateto);

                $scope.model.filters = $scope.report.config.body;

                $scope.list.get();

            }, function (error) {
                $scope.error = error;
                growl.error(error);
            });
        };

        $scope.createReport = function () {
            var start_time = toUTC(moment($scope.list.range.dateFrom).format('YYYY-MM-DD 00:00:00'));
            var end_time = toUTC(moment($scope.list.range.dateTo).format('YYYY-MM-DD 23:59:59'));

            var report = angular.copy($scope.report);
            report.global = $scope.report.global ? 1 : 0;
            report.config = {
                url: {
                    "datefrom": start_time,
                    "dateto": end_time
                },
                body: $scope.model.filters
            };

            if ($scope.id != null) {
                ReportService.update($scope.id, report).then(function (data) {
                    $log.log(data);
                    growl.success("report_updated_successfully");

                    $rootScope.$broadcast('reports-updated');

                }, function (error) {
                    $scope.error = error;
                    growl.error(error);
                });
            } else {
                ReportService.create(report).then(function (data) {
                    $log.log(data);
                    growl.success("report_created_successfully");

                    $rootScope.$broadcast('reports-updated');

                }, function (error) {
                    $scope.error = error;
                    growl.error(error);
                });
            }
        };

        if ($scope.id != null) {
            $scope.getReport($scope.id);
        }

    });
