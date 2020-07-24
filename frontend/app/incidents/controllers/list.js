'use strict';

angular.module('app')
    .controller('IncidentCtrl', function ($scope, $location, $state, $rootScope, $sce, $timeout, $log, $window, $intercom, $filter,  IncidentService, DateRangeService, currentUser, growl, ApiService, CONFIG, LS, questions) {


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
            dashboard_feature_last_used: "Incidents"
        });

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        var date_format = $scope.datetime_format.slice(0,10);
        $scope.date_format = date_format_mapping[date_format];

        var current = new Date();
        var tz = jstz.determine();

        var tabs = questions.DashboardItems;
        var defaults = {};
        for (var key in tabs) {
            if (tabs.hasOwnProperty(key)) {
                for (var question in tabs[key]) {
                    if (tabs[key].hasOwnProperty(question)
                        && (question == 'Questions')) {
                        for (var m in tabs[key][question]) {
                            if (tabs[key][question].hasOwnProperty(m)) {
                                var q = tabs[key][question][m];
                                if (q.hasOwnProperty("Default")) {
                                    defaults[m] = tabs[key][question][m]["Default"];
                                }
                            }
                        }
                    }
                }
            }
        }

        function toUTC(value) {
            return moment.tz(value, $scope.datetime_format, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format($scope.datetime_format);
        }

        var resort = currentUser.resorts[0];
        var resort_id = resort.resort_id;

        DateRangeService.range = {
             dateFrom: DateRangeService.range.dateFrom,
             dateTo: DateRangeService.range.dateTo
        };

        $scope.list = {
            range: DateRangeService.range,
            incidents: [],
            currentPage: 1,
            itemsPerPage: 100,
            totalItems: 0,
            totalPages: 0,
            predicate: 'dt_created',
            reverse: true,
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

                $scope.list.get();
            },

            get: function () {
                $log.log('fetching incidents...');

                $scope.list.loading = true;

                var start_time = toUTC(moment($scope.list.range.dateFrom).format(date_format + ' 00:00:00'));
                var end_time = toUTC(moment($scope.list.range.dateTo).format(date_format + ' 23:59:59'));


                IncidentService.fetchList(start_time, end_time, resort_id, $scope.list.itemsPerPage, $scope.list.currentPage, $scope.list.predicate, $scope.list.reverse).then(function (data) {

//                    $log.log(data.results);

                    $scope.list.loading = false;

                    var incidents = data.results.map(function (incident) {
                        incident.dt_created = toLocalTime(incident.dt_created);
                        incident.patient_name = incident.patient.name;
                        incident.injury_name = $filter('transformInjury')(incident.injury);
                        incident.assigned_to_name = incident.assigned_to.name;
                        incident.status = incident.incident_status[0].key;
                        return incident;
                    });

//                    $log.log(incidents);

                    $scope.list.incidents = incidents;
                    $scope.list.totalItems = data.count;
                    $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);

                }, function (reason) {

                    $rootScope.on_error(reason);
                    $scope.list.incidents = [];
                    $scope.list.success = false;
                    $scope.list.error = reason.errors.Error;
                    $scope.list.loading = false;
                });
            },

            add: function () {
                growl.info('ADDING_INCIDENT');
                var default_data = {"field_52ca456962ba8": {
                    "lat": resort.map_lat,
                    "long": resort.map_lng,
                    "accuracy": 16
                }};

                $.extend(default_data, defaults);
                IncidentService.createIncident(default_data).then(function (data) {
                    growl.info('INCIDENT_ADDED');
                    $scope.list.get();
                }, function (reason) {
                });
            },

            print: function (id) {
                $log.log('printing incident ' + id);
                growl.info('PRINTING');

                if (id !== null || id !== undefined) {
                    var xhr = new XMLHttpRequest();

                    // Use JSFiddle logo as a sample image to avoid complicating
                    // this example with cross-domain issues.
                    xhr.open("GET", ApiService.base() + CONFIG.API_URL + '/incidents/' + id + '/print/?timestamp=' + new Date().getTime(), true);

                    var authorization = LS.get('Authorization');
                    var token = LS.get('token');

                    xhr.setRequestHeader('Authorization', authorization);
                    xhr.setRequestHeader('token', token);

                    // Ask for the result as an ArrayBuffer.
                    xhr.responseType = "arraybuffer";

                    xhr.onload = function (e) {
                        // Obtain a blob: URL for the image data.
                        var arrayBufferView = new Uint8Array(this.response);
                        var blob = new Blob([ arrayBufferView ], { type: 'application/pdf' });
                        var urlCreator = window.URL || window.webkitURL;
                        var fileURL = urlCreator.createObjectURL(blob);
                        fileURL = $sce.trustAsResourceUrl(fileURL);
                        var downloadfilename = id+".pdf";

                        var anchor = angular.element('<a/>');
                        anchor.attr({
                            href: fileURL,
                            target: '_blank',
                            download: downloadfilename
                        })[0].click();
                    };

                    xhr.send();


//                    IncidentService.print(id)
//                        .then(function (data) {
//                            var arrayBufferView = new Uint8Array(data);
//                            var blob = new Blob([ arrayBufferView ], { type: 'application/pdf' });
//                            var urlCreator = window.URL || window.webkitURL;
//                            var fileURL = urlCreator.createObjectURL(blob);
//                            fileURL = $sce.trustAsResourceUrl(fileURL);
//                            var downloadfilename = id+".pdf";
//
//                            var anchor = angular.element('<a/>');
//                            anchor.attr({
//                                href: fileURL,
//                                target: '_blank',
//                                download: downloadfilename
//                            })[0].click();
//
//                        }, function (error) {
//                            $scope.error = error;
//                        });
                }

            }
        };

        console.log($scope.list);

        $scope.$watch(
            'list.range.dateFrom',
            function (newValue, oldValue) {
                if (newValue !== oldValue && newValue != undefined) {
                    $scope.list.get();
                }
            }
        );

        $scope.$watch(
            'list.range.dateTo',
            function (newValue, oldValue) {
                if (newValue !== oldValue && newValue != undefined) {
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
    });