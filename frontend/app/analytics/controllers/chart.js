'use strict';

angular.module('app')
    .controller('ChartCtrl', function ($scope, $location, $state, $stateParams, $rootScope, $timeout, $log, $q, $window, $intercom, $translate, IncidentService, DateRangeService, questions, currentUser, growl, ReportService) {

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
            dashboard_feature_last_used: "Charts"
        });

        var current = new Date();
        var tz = jstz.determine();

        var resort = currentUser.resorts[0];
        var resort_id = resort.resort_id;

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = resort.datetime_format.key;
        var date_format = $scope.datetime_format.slice(0, 10);
        $scope.date_format = date_format_mapping[date_format];

        function toUTC(value) {
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format(date_format);
        }

        $scope.id = $stateParams.reportId;

        $scope.scales = [
            {key: 'date', value: 'Date'},
            {key: 'day', value: 'Day'},
            {key: 'hour', value: 'Hour'},
            {key: 'day_of_week', value: 'Weekday'},
            {key: 'week_of_year', value: 'Week of Year'},
            {key: 'month_of_year', value: 'Month'},
            {key: 'year', value: 'Year'},
            {key: 'hour_of_day_of_week', value: 'Hour of Day of Week'}
        ];

        $scope.scale = $scope.scales[0];

        $scope.schema = {
            type: "object",
            properties: [],
            properties_alter: []
        };

        $scope.schema.properties_alter.push({
            'title': 'Incidents - Total',
            'type': 'string',
            'order': 0,
            'fullkey': 'total_incident',
            'key': 'total_incident',
            'formtype': 'select',
            'placeholder': '',
            'titleMap': []
        });


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
            'range',
            'arrows',
            'select',
            'multi_select',
            'radio',
            'radio_button',
            'gender'
        ];

        var tabs = questions.DashboardItems;

        var getChoiceMap = function (mapValues) {
            var _choices = [],
                _titlemap = [];

            // Loop and build choices and titlemap
            angular.forEach(mapValues, function (value) {
                for (var key in value) {
                    //console.log(value[key]);
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
                                    if (!q.hasOwnProperty('ParentKey') || (q.hasOwnProperty('ParentKey') && tabs[key][question].hasOwnProperty(q['ParentKey']))) {
                                        if (q.hasOwnProperty('ParentKey')) {
                                            temp_schema_properties_question.forEach(function (current, index, array) {
                                                if (current.key == q['ParentKey']) {
                                                    var fullkey = m;

                                                    if (question == 'RepeatingQuestions') {
                                                        fullkey = key + '____' + m;
                                                    }

                                                    if (current.hasOwnProperty('childField')) {
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
                                                    else {
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
                                        else {
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
                                }

                                else {
                                    if (q.Type == "repeater" && q.hasOwnProperty('RepeatingQuestions')) {
                                        for (var question1 in tabs[key][question][m]) {
                                            if (tabs[key][question][m].hasOwnProperty(question1) && (question1 == 'Questions' || question1 == 'RepeatingQuestions')) {
                                                var temp_schema_properties = [];
                                                for (var n in tabs[key][question][m][question1]) {
                                                    if (tabs[key][question][m][question1].hasOwnProperty(n)) {

                                                        var q1 = tabs[key][question][m][question1][n];

                                                        choices = [];
                                                        titlemap = [];

                                                        if (q1.Type == 'select' || q1.Type == 'multi_select' || q1.Type == 'arrows') {

                                                            for (var key11 in q1.Values) {

                                                                if (q1.Values.hasOwnProperty(key11)) {

                                                                    choiceMap = getChoiceMap(q1.Values);

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
                                                                        'fullkey': m + '____' + n,
                                                                        'key': n,
                                                                        'formtype': form_type[q1.Type],
                                                                        'placeholder': $translate.instant(q1.Placeholder),
                                                                        'titleMap': titlemap
                                                                    });
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                $scope.schema.properties = $scope.schema.properties.concat(temp_schema_properties);
                                                $scope.schema.properties_alter = $scope.schema.properties_alter.concat(temp_schema_properties);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        $scope.schema.properties = $scope.schema.properties.concat(temp_schema_properties_question);
                        $scope.schema.properties_alter = $scope.schema.properties_alter.concat(temp_schema_properties_question);
                    }
                }
            }
        }

        $scope.onSubmit = function (form) {
            $scope.list.get();
        };

        $scope.onDownload = function (form) {
            $scope.onProcess($scope.chart_type);

            //console.log($scope.finalmodel[0].data);

            if (angular.equals({}, $scope.finalmodel[0].data)) {
                growl.error("Atleast one filter must be selected to proceed");
            } else {

                IncidentService.fetchChartCSV($scope.finalmodel, $scope.chart_type, resort_id, 'csv').then(
                    function (data) {
                        //$log.log(data);

                        var anchor = angular.element('<a/>');
                        anchor.attr({
                            href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                            target: '_blank',
                            download: 'chart.csv'
                        })[0].click();
                    }
                );
            }
        };

        $scope.chart_type = 'timeline';

        $scope.model = [
            {
                compare: true,
                date: {
                    datefrom: DateRangeService.range.dateFrom,
                    dateto: DateRangeService.range.dateTo
                },
                data: [
                    {}
                ]
            },
            {
                compare: false,
                date: {
                    datefrom: DateRangeService.range.dateFrom,
                    dateto: DateRangeService.range.dateTo
                },
                data: [
                    {}
                ]
            }
        ];

        $scope.finalmodel = null;

        $scope.addField = function (filters) {
            filters.push({});
        };

        $scope.removeField = function (filters, index) {
            filters.splice(index, 1);
        };


        $scope.onReset = function () {
            $scope.model = [
                {
                    compare: true,
                    date: {
                        datefrom: DateRangeService.range.dateFrom,
                        dateto: DateRangeService.range.dateTo
                    },
                    data: [
                        {}
                    ]
                },
                {
                    compare: false,
                    date: {
                        datefrom: DateRangeService.range.dateFrom,
                        dateto: DateRangeService.range.dateTo
                    },
                    data: [
                        {}
                    ]
                }
            ];
        };


        $scope.onProcess = function (chart_type) {
            $scope.finalmodel = [];

            var diffDays = 0;

            angular.forEach($scope.model, function (model_filter, key) {

                if (model_filter.compare) {
                    var a = moment(model_filter.date.datefrom);
                    var b = moment(model_filter.date.dateto);

                    if (key == 0) {
                        diffDays = b.diff(a, 'days');
                    } else {
                        b = angular.copy(a);
                        b.add(diffDays, 'days');
                    }

                    var start_time = toUTC(a.format('YYYY-MM-DD 00:00:00'));
                    var end_time = toUTC(b.format('YYYY-MM-DD 23:59:59'));


                    var date = {
                        'datefrom': start_time,
                        'dateto': end_time
                    };

                    var filters = {};

                    console.log(model_filter.data);

                    if(chart_type != 'pie') {
                        angular.forEach(model_filter.data, function (value, key) {
                            if (value && value.field && value.field.fullkey) {
                                filters[value.field.fullkey] = filters[value.field.fullkey] || [];
                                filters[value.field.fullkey].push(value.value);

                                if (value.hasOwnProperty('childField') && value.childField.value && (value.childField.value != 'all')) {
                                    filters[value.childField.field.fullkey] = filters[value.childField.field.fullkey] || [];
                                    filters[value.childField.field.fullkey].push(value.childField.value);
                                }
                            }
                        });
                    }
                    else{
                        angular.forEach(model_filter.data, function (value, key) {
                            if (value && value.field && value.field.fullkey) {
                                if(value.field.hasOwnProperty('childField') && value.value && value.field.childField.hasOwnProperty(value.value)){
                                    filters[value.field.childField[value.value].fullkey] = filters[value.field.childField[value.value].fullkey] || [];
                                    filters[value.field.childField[value.value].fullkey].push("");
                                }
                                else{
                                    filters[value.field.fullkey] = filters[value.field.fullkey] || [];
                                    filters[value.field.fullkey].push("");

                                    value.value = "";
                                }
                            }
                        });
                    }

                    var model =
                        {
                            date: date,
                            data: filters,
                            scale: $scope.scale.key
                        }
                        ;

                    if (chart_type == 'pie') {
                        if ($scope.finalmodel.length < 1) {
                            $scope.finalmodel.push(model);
                        }
                    } else {
                        $scope.finalmodel.push(model);
                    }

                }
            });
        };

        $scope.$watch(
            'model',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.onProcess($scope.chart_type);
                }
            },
            true
        );

        $scope.css = "height:400px;background-color:transparent;";


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

            get: function () {
                $log.log('fetching incidents...');
                $scope.list.loading = true;

                $scope.onProcess($scope.chart_type);

                //console.log($scope.finalmodel[0].data);

                if (angular.equals({}, $scope.finalmodel[0].data)) {
                    growl.error("Atleast one filter must be selected to proceed");
                } else {

                    IncidentService.fetchChart($scope.finalmodel, $scope.chart_type, resort_id).then(
                        function (data) {

                            if ($scope.chart_type == 'timeline' || $scope.chart_type == 'bar') {

                                var columns = 1;

                                if (data.length > 0) {
                                    columns = data[0].length;
                                }


                                $scope.columns = [];
                                $scope.rows = [];

                                var cols = [
                                    {id: "date", label: $scope.scale.value, type: "string", 'role': 'domain'}
                                ];

                                for (var i = 0; i < columns; i++) {
                                    cols.push({id: "count", label: "Count", type: "number"});

                                    //tooltip
                                    cols.push({type: "string", 'role': 'tooltip', 'p': {'html': true}});

                                    $scope.columns.push($scope.scale.value);
                                    $scope.columns.push('Incident Count');
                                }

                                if (columns > 1) {
                                    $scope.columns.push('Deviation');
                                }

                                var rows = data.map(function (item, index) {
                                    var c = [];

                                    if ($scope.scale.key == 'date') {
                                        c.push({v: moment(item[0].columndetail, 'YYYY-MM-DD').format(date_format)});
                                    }
                                    else {
                                        c.push({v: item[0].columndetail});
                                    }

                                    //if ($scope.scale.key == 'date') {
                                    //    c.push({v: item[0].columndetail});
                                    //} else {
                                    //    c.push({v: item[0].columndetail});
                                    //}

                                    var tooltip = '';

                                    var row = [];
                                    for (var i = 0; i < columns; i++) {
                                        c.push({v: item[i].count});
                                        tooltip = '<p style="width:100px;padding:5px;"><strong> ' + item[i].columndetail + '</strong><br/><strong> Count:</strong> ' + item[i].count + '</p>';
                                        //tooltip
                                        c.push({v: tooltip});

                                        if ($scope.scale.key == 'date') {
                                            row.push(moment(item[i].columndetail, 'YYYY-MM-DD').format(date_format));
                                        }
                                        else {
                                            row.push(item[i].columndetail);
                                        }

                                        row.push(item[i].count);
                                    }

                                    if (columns > 1) {
                                        row.push(((row[3] - row[1]) * 100 / (row[3] == 0 ? 1 : row[3])).toFixed(0) + '%');
                                    }

                                    $scope.rows.push(row);

                                    return {
                                        c: c
                                    }
                                });

                                var chart_map = {
                                    'timeline': 'LineChart',
                                    'bar': 'ColumnChart',
                                    'pie': 'PieChart'
                                };

                                $scope.chart = {
                                    type: chart_map[$scope.chart_type],
                                    data: {
                                        "cols": cols,
                                        "rows": rows
                                    },

                                    options: {
//              "title": "Incidents",
//              "fill": 20,
                                        pieHole: 0.5,
                                        "displayExactValues": true,
                                        "vAxis": {
                                            "title": "Incidents", "gridlines": {"count": 6}
                                        },
//                                focusTarget: 'category',
                                        tooltip: {isHtml: true},
                                        "hAxis": {
                                            "title": $scope.scale.value
                                        },
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
                            } else {

                                // PIE chart

                                $scope.columns = [
                                    $scope.model[0].data[0].field.title,
                                    "Count"
                                ];

                                $scope.rows = data.map(function (item) {
                                    return [
                                        $translate.instant(item.name),
                                        item.count

                                    ]
                                });


                                var rows = data.map(function (item) {
                                    return {
                                        c: [
                                            {v: $translate.instant(item.name)},
                                            {v: item.count}
                                        ]
                                    }
                                });

                                //console.log($scope.model[0].data[0].field.title);
                                //console.log(rows);

                                $scope.chart = {
                                    type: "PieChart",
                                    data: {
                                        "cols": [
                                            {id: "name", label: $scope.model[0].data[0].field.title, type: "string"},
                                            {id: "count", label: "Count", type: "number"}
                                        ], "rows": rows
                                    },

                                    options: {
//                "title": "Incidents",
                                        pieHole: 0.5,
//                "fill": 20,
                                        "displayExactValues": true,
                                        "vAxis": {
                                            "title": "Count of Incidents"
                                        },
                                        "hAxis": {
                                            "title": $scope.model[0].data[0].field.title
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


                            $scope.list.loading = false;

                            $scope.list.incidents = data;
                            $scope.list.filteredItems = ($scope.list.incidents == null) ? 0 : $scope.list.incidents.length; //Initially for no filter
                            $scope.list.totalItems = data.length;
                            $scope.list.totalPages = 1;
//                        $scope.list.sort_by('dt_created');
//                        $scope.list.reverse = true;

                        }, function (reason) {

                            $rootScope.on_error(reason);
                            $scope.list.incidents = [];
                            $scope.list.success = false;
                            $scope.list.error = reason.errors.Error;
                            $scope.list.loading = false;
                        });
                }
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

//        $scope.$watch(
//            'list.itemsPerPage',
//            function (newValue, oldValue) {
//                if (newValue !== oldValue) {
//                    $scope.list.get();
//                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
//                }
//            }
//        );
//
//        $scope.$watch(
//            'list.currentPage',
//            function (newValue, oldValue) {
//                if (newValue !== oldValue) {
//                    $scope.list.get();
//                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
//                }
//            }
//        );

        //$scope.report = {
        //    "config": {
        //        "url": {
        //            "daterange": "-7d",
        //            "group_by": "field_52ca430462b9a",
        //            "group_by_2": "field_54b084fb2d255",
        //            "compare_with": "field_52ca3fcc59d29",
        //            "datecomparefrom": "2015-04-21 07:38:15",
        //            "datecompareto": "2015-04-22 07:38:15",
        //            "datecomparerange": "-7d",
        //            "display": "field_52d47a654d1fc",
        //            "compare_to": "field_52ca3fcc59d29",
        //            "show_count": 5
        //        },
        //        "body": {
        //            "name": ["Krish", "Shaun"],
        //            "occupation": ["Software Developer", "Painter"],
        //            "notes____field_52ca448dg94ja3": ["new note"],
        //            "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
        //            "field_52ca456962ba8____long": ["144.96191799999997"],
        //            "field_52ca445d62ba6": ["Good"],
        //            "field_52dd8c049b005": [50],
        //            "field_52ca445d62ba1": ["23"],
        //            "field_52d4798f6d227____preexisting_injury": ["817", "820"]
        //        }
        //    }
        //};

        $scope.report = {
            label: "",
            global: 0,
            type: 'timeline',
            config: {
                url: {},
                body: {}
            }
        };

        $scope.getReport = function (id) {
            ReportService.fetch(id).then(function (data) {
                $log.log(data);

                growl.success("chart_fetched_successfully");

                $scope.report = data;
                $scope.chart_type = $scope.report.type;
                $scope.report.global = $scope.report.global > 0;
                $scope.list.range.dateFrom = toLocalTime($scope.report.config.url.datefrom);
                $scope.list.range.dateTo = toLocalTime($scope.report.config.url.dateto);

                $scope.model = $scope.report.config.body;

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
            report.type = $scope.chart_type;
            report.config = {
                url: {
                    "datefrom": start_time,
                    "dateto": end_time
                },
                body: $scope.model
            };

            if ($scope.id != null) {
                ReportService.update($scope.id, report).then(function (data) {
                    $log.log(data);
                    growl.success("chart_updated_successfully");

                    $rootScope.$broadcast('reports-updated');

                }, function (error) {
                    $scope.error = error;
                    growl.error(error);
                });
            } else {
                ReportService.create(report).then(function (data) {
                    $log.log(data);
                    growl.success("chart_created_successfully");

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
