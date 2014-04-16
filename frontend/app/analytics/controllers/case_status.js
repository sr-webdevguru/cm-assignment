'use strict';

angular.module('app')
    .controller('CaseStatusCtrl', function ($scope, $location, $state, $stateParams, $rootScope, $timeout, $log, $q, $window, $intercom, $translate, IncidentService, DateRangeService, currentUser, growl, incidentStatus, filterFilter) {

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
            dashboard_feature_last_used: "CaseStatus"
        });

        var date_format_mapping = {
            "MM/DD/YYYY": "MM/dd/yyyy",
            "DD/MM/YYYY": "dd/MM/yyyy"
        };

        var resort = currentUser.resorts[0];
        $scope.datetime_format = resort.datetime_format.key;
        var date_format = $scope.datetime_format.slice(0, 10);
        $scope.date_format = date_format_mapping[date_format];
        var tz = jstz.determine();

        function toUTC(value) {
            if (typeof value === 'object') {
                try { value = value.format(); } catch (e){ value = JSON.stringify(value); }
            }
            return moment.tz(value, 'YYYY-MM-DD HH:mm:ss', tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format(date_format);
        }

        $scope.date_range_options = [
            {
                "name": $translate.instant("last_seven_days"),
                "value": "a"
            },
            {
                "name": $translate.instant("last_thirty_days"),
                "value": "b"
            },
            {
                "name": $translate.instant("last_six_months"),
                "value": "c"
            },
            {
                "name": $translate.instant("last_twelve_months"),
                "value": "d"
            },
            {
                "name": $translate.instant("custom_date_range"),
                "value": "e"
            }
        ];

        $scope.selected_date_range_option = "b";

        $scope.datefrom = moment().subtract(30, 'days'); // + 'T00:00:00.000Z';
        $scope.dateto = moment();//.tz(tz.name()).format('YYYY-MM-DD')+ 'T23:59:59.999Z';

        $scope.incidentStatus = [];

        $scope.incidentStatus = incidentStatus.map(function(currentValue, Index){
            if(currentValue.order == 9){

            }
            else if(currentValue.order == 8){
                currentValue["selected"] = false;
                return currentValue
            }
            else{
                currentValue["selected"] = true;
                return currentValue
            }
        });
        $scope.incidentStatus.pop();

        // selected fruits
        $scope.selectedStatus = [];

        // watch fruits for changes
        $scope.$watch('incidentStatus|filter:{selected:true}', function (nv) {
            $scope.selectedStatus = nv.map(function (status) {
                return status.order;
            });
        }, true);

        // Watch datefrom and dateto
        $scope.$watch('selected_date_range_option', function(nv) {
            switch(nv.value) {
                case 'a':
                    $scope.datefrom = moment().subtract(7, 'days');
                    break;
                case 'b':
                    $scope.datefrom = moment().subtract(30, 'days');
                    break;
                case 'c':
                    $scope.datefrom = moment().subtract(180, 'days');
                    break;
                case 'd':
                    $scope.datefrom = moment().subtract(1, 'year');
                    break;
                case 'e':
                    break;
            }
        }, true);

        $scope.list = {
            incidents: [],
            summary: [],
            currentPage: 1,
            itemsPerPage: 20,
            filteredItems: 0,
            totalItems: 0,
            totalPages: 0,
            loading: false,
            success: true,
            error: ''
        };

        $scope.search = function(){

            IncidentService.fetchStatusReport(toUTC($scope.datefrom), toUTC($scope.dateto), $scope.selectedStatus.toString(), $scope.list.itemsPerPage, $scope.list.currentPage, 'json').then(
                function (data) {
                    $scope.list.loading = false;

                    angular.forEach(data.results, function(elem, index) {
                        data.results[index]['dt_created'] = toLocalTime(moment(elem['dt_created'], 'YYYY-MM-DD HH:mm:ss'));
                    });

                    $scope.list.incidents = data.results;
                    $scope.list.summary = data.summary;
                    $scope.list.filteredItems = ($scope.list.incidents == null) ? 0 : $scope.list.incidents.length; //Initially for no filter
                    $scope.list.totalItems = data.count;
                    $scope.list.totalPages = Math.ceil(data.count / $scope.list.itemsPerPage);

                    var max_count = data.summary.reduce(function(a,b){
                        return a.count > b.count ? a : b
                    });

                    angular.forEach($scope.list.summary, function(elem, index) {
                        if(elem.count != max_count.count) {
                            $scope.list.summary[index]['width'] = max_count.count != 0 ? ((elem.count * 100) / max_count.count) + 25 : 25;
                            $scope.list.summary[index]['height'] = max_count.count != 0 ? ((elem.count * 100) / max_count.count) + 25 : 25;
                        }
                        else{
                            $scope.list.summary[index]['width'] = max_count.count != 0 ? ((elem.count * 100) / max_count.count) : 25;
                            $scope.list.summary[index]['height'] = max_count.count != 0 ? ((elem.count * 100) / max_count.count) : 25;
                        }
                    });
                }
            )};

        $scope.statusFilter = function(id){
            $scope.selectedStatus = id;
            $scope.incidentStatus = $scope.incidentStatus.map(function(currentValue, Index){
                if(currentValue.order == id){
                    currentValue["selected"] = true;
                    return currentValue
                }
                else{
                    currentValue["selected"] = false;
                    return currentValue
                }
            });
            $scope.search();
        };

        $scope.onPrint = function(){
            $window.print();
        };

        $scope.onDownload = function(){
            IncidentService.fetchStatusReport(toUTC($scope.datefrom), toUTC($scope.dateto), $scope.selectedStatus.toString(), $scope.list.itemsPerPage, $scope.list.currentPage, 'csv').then(
                function(data) {
                    var anchor = angular.element('<a/>');
                    anchor.attr({
                        href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                        target: '_blank',
                        download: 'status-report.csv'
                    })[0].click();
                })
        };

        $scope.$watch(
            'list.itemsPerPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.search();
                }
            }
        );

        $scope.$watch(
            'list.currentPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.search();
                }
            }
        );

    });