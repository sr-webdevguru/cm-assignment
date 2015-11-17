'use strict';

angular.module('app')
    .controller('MapCtrl', ['$scope', '$rootScope', '$state', '$location', '$timeout', '$log', '$filter',
        '$intercom', 'UserService', 'QuestionService', 'currentUser', 'IncidentService', 'growl', 'hotkeys',
        '$http', 'questions', '$translate', '$uimodal', 'LS', 'ResortService', 'settings',
        function ($scope, $rootScope, $state, $location, $timeout, $log, $filter, $intercom, UserService,
                  QuestionService, currentUser, IncidentService, growl, hotkeys, $http, questions,
                  $translate, $modal, LS, ResortService, settings) {

        if (currentUser.role == "Patroller") {
            $state.go("incidents");
        }
        var urlBase = $location.protocol() + '://' + $location.host();
        if ($location.port()) urlBase+= ':' + $location.port();
        urlBase += '/images/';
        var style_lifts = {
            "strokeColor": "#ff0000",
            "fillColor": "#ff0000",
            "fillOpacity": 0.5,
            "dashArray": "15,5",
            "strokeWeight": "3"
        };
        var style_buildings = {
            "strokeColor": "#0000ff",
            "fillColor": "#0000ff",
            "fillOpacity": 0.5,
            "strokeWeight": "1"
        };
        var style_red = {
            "strokeColor": "#ff0000",
            "fillColor": "#ff0000",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };
        var style_green = {
            "strokeColor": "#00ff00",
            "fillColor": "#00ff00",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };
        var style_blue = {
            "strokeColor": "#0000ff",
            "fillColor": "#0000ff",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };
        var style_doubleblue = {
            "strokeColor": "#0000ff",
            "fillColor": "#0000ff",
            "dashArray": "15,10,1,10,1,10",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };
        var style_black = {
            "strokeColor": "#000000",
            "fillColor": "#000000",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };
        var style_doubleblack = {
            "strokeColor": "#000000",
            "fillColor": "#000000",
            "dashArray": "15,10,1,10,1,10",
            "fillOpacity": 0.5,
            "strokeWeight": "3"
        };

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
            dashboard_feature_last_used: "Map"
        });

        var current = new Date();
        var tz = jstz.determine();
        $scope.tz = tz.name();

        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        $scope.date_format = $scope.datetime_format.slice(0,10);

        var diff = new Date(current.getTime());// - (7 * 24 * 60 * 60 * 1000));
        var local_start = moment.tz(diff, tz.name()).format('YYYY-MM-DD 00:00:00');
        var local_end = moment.tz(diff, tz.name()).format('YYYY-MM-DD 23:59:59');

        var start = moment.tz(local_start, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        var end = moment.tz(local_end, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');

        var resort_id = currentUser.resorts[0].resort_id;
        var update_incident = false;
        var list_incidents = true;
        var selected_incident_pk = null;
        $scope.datetime_format = currentUser.resorts[0].datetime_format.key;
        $scope.date_format = $scope.datetime_format.slice(0,10);

        $scope.userConnected = currentUser.user_connected.key;
        $scope.incidentToHighlight = 0;
        $scope.tempIncidentPk = 0;


        $scope.schema = {
            type: "object",
            properties: []
        };


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
                    if(key.indexOf("controlled") < 0) {
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
        $scope.googleMapMarkers = [];
        $scope.findMarker = function(marker){
            return $scope.googleMapMarkers.find(function(googleMapMarker){
                return marker.location.toString() === googleMapMarker.incident.location.toString() &&
                    marker.dt_created === googleMapMarker.incident.dt_created;
            });
        };
        $scope.relocateMarkers = function(){
            var foundDuplicates = [];
            var markersCopy = angular.copy($scope.map.markers);
            var foundIdx = 1;
            markersCopy.map(function(location, i) {
                markersCopy.map(function(nextLocation, j){
                    if (j <= i) return;
                    var found;
                    var deltaLat = (nextLocation.lat - location.lat);
                    var deltaLng = (nextLocation.lng - location.lng);
                    if (deltaLat < .00002) {
                        if (deltaLng < .00002) found = [1,1];
                        else if ((deltaLng * -1) < .00002) found = [1,-1];
                    } else if ((deltaLat * -1) < .00002){
                        if (deltaLng < .00002) found = [-1,1];
                        else if ((deltaLng * -1) < .00002) found = [-1,-1];
                    }
                    if (!found) return;
                    markersCopy[j].lng = markersCopy[j].lng + ((.00003));
                    foundDuplicates.push(j);
                    return;
                });
            });
            markersCopy.map(function(location, i) {
                // var foundDuplicate =
                var compass = Math.cos(((foundDuplicates.length * foundIdx)/36) );
                foundIdx++;
                markersCopy[i].lat = markersCopy[i].lat + (compass  * .00002);
            });
            return markersCopy;
        };
        $scope.getIncidentFromRelocatedMarker = function(incident){
            var markers = $scope.relocateMarkers();
            var found = markers.find(function(marker){
                if (!marker.incident) return;
                return incident.header === marker.incident.header;
            });
            if (found) return found;
            incident.lat = incident.location.lat;
            incident.lng = incident.location.long;
            return incident;
        };
        $scope.initMap = function(resize){
            $scope.googleMap = new google.maps.Map(document.getElementById('map'), {
              zoom: $scope.map.center.zoom,
              center: {lat: $scope.map.center.lat, lng: $scope.map.center.lng }
            });

            if (currentUser && currentUser.resorts.length > 0 && currentUser.resorts[0].map_kml) {
                var getRatingStyle = function (color, g){
                    switch(color){
                        case 'green': return data.style_green? parseStyle(data.style_green, g): style_green;
                        case 'red': return data.style_red? parseStyle(data.style_red, g): style_red;
                        case 'blue': return data.style_blue? parseStyle(data.style_blue, g): style_blue;
                        case 'doubleblue': return data.style_doubleblue? parseStyle(data.style_doubleblue, g):
                            style_doubleblue;
                        case 'black': return data.style_black? parseStyle(data.style_black, g): style_black;
                        case 'doubleblack': return data.style_doubleblack? parseStyle(data.style_doubleblack, g) :
                            style_doubleblack;
                    }
                };
                var parseStyle = function(style, geometry){
                    var result = {
                        fillColor: style.color,
                        fillOpacity: 0.5,
                        strokeColor: style.color,
                        strokeWeight: style.weight
                    }
                    if (!style.dashArray || style.dashArray.length === 0) return result;

                    var path = '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1">';
                    path+= '<line stroke-dasharray="' + style.dashArray + '" ';
                    var x = 1;
                    var y = 1;
                    geometry.forEachLatLng(function(g){
                        path+= 'x' + x + '="' + g.lat() + '" y' + y + '="' + g.lng() + '"';
                        x++; y++;
                    });
                    path+= '/></svg>';
                    result.icon = { path: path };
                    return result;

                };
                var data = settings.geojson;
                if (!data) data = {};
                if (!data.buildings || !data.buildings.features) data.buildings = { features: [] };
                if (!data.runs || !data.runs.features) data.runs = { features: [] };
                if (!data.lifts || !data.lifts.features) data.lifts = { features: [] };

                data.buildings.features = data.buildings.features.map(function(feature){
                    feature.properties.ownerSet = 'BUILDINGS';
                    return feature;
                });
                data.runs.features = data.runs.features.map(function(feature){
                    feature.properties.ownerSet = 'RUNS';
                    return feature;
                });
                data.lifts.features = data.lifts.features.map(function(feature){
                    feature.properties.ownerSet = 'LIFTS';
                    return feature;
                });
                $scope.googleMap.data.addListener('click', function(event){
                    var feature = event.feature.f;
                    var infowindow = new google.maps.InfoWindow({
                      content: feature.description,
                        position: {
                          lat: event.latLng.lat(),
                          lng: event.latLng.lng()
                        }
                    });
                    infowindow.open($scope.googleMap);
                });
                $scope.googleMap.data.addGeoJson(data.buildings);
                $scope.googleMap.data.addGeoJson(data.runs);
                $scope.googleMap.data.addGeoJson(data.lifts);
                $scope.googleMap.data.setStyle(function(feature) {
                    var geometry = feature.getGeometry();
                    switch(feature.getProperty('ownerSet').toUpperCase()){
                        case 'BUILDINGS':
                            return data.style_buildings? parseStyle(data.style_buildings, geometry) : style_buildings;
                        case 'RUNS':
                            return getRatingStyle(feature.getProperty('rating')? feature.getProperty('rating') : '', geometry);
                        case 'LIFTS':
                            return data.style_lifts? parseStyle(data.style_lifts, geometry) : style_lifts;
                    }
                });
            }
            google.maps.event.addListener($scope.googleMap, "rightclick", function(event) {
                var lat = event.latLng.lat();
                var lng = event.latLng.lng();
                $scope.list.add(lat, lng);
            });
            google.maps.event.addListener($scope.googleMap, "click", function(event) {
                angular.forEach($scope.incidents, function (incident) {
                    incident.selected = false;
                });
                $scope.info.isOpen = false;
            });
            if (resize) google.maps.event.trigger($scope.googleMap, 'resize');
            var markersCopy = $scope.relocateMarkers();
            var markers = markersCopy.map(function(location, i) {
                var id = location.incident.header.split(',')[0];
                var marker =  new google.maps.Marker({
                    icon: urlBase + 'pin_' + location.incident.incident_status[0].color + '.png',
                    position: location,
                    label: id,
                    draggable: true
                });
                marker.incident = location.incident;
                google.maps.event.addListener(marker, 'click', function() {
                    $scope.highlight(this.incident);
                });
                google.maps.event.addListener(marker, 'dragend', function(point) {
                    IncidentService.updateIncident(this.incident.incident_id, {
                        "field_52ca456962ba8": {
                            lat: point.latLng.lat(),
                            long: point.latLng.lng()
                        }
                    }).then(function (data) {
                            growl.info("Incident location updated");
                        }, function (error) {
                            growl.error("incident_update_failed");
                    });
                });
                $scope.googleMapMarkers.push(marker);
                return marker;
            });
            $scope.googleMapCluster = new MarkerClusterer($scope.googleMap, markers, {
                imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
            });
        };

        $scope.question_items = [];

        $scope.form_items = [];
        var defaults = {};

        for(var key in tabs) {
            if (tabs.hasOwnProperty(key)) {
                for (var question in tabs[key]) {
                    if (tabs[key].hasOwnProperty(question) && (question == 'Questions' || question == 'RepeatingQuestions')) {

                        for (var m in tabs[key][question]) {
                            if (tabs[key][question].hasOwnProperty(m)) {


                                var q = tabs[key][question][m];

                                if (q.hasOwnProperty("Default")) {
                                    defaults[m] = tabs[key][question][m]["Default"];
                                }

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
                                        value: "male",
                                        name: "Male"
                                    });

                                    titlemap.push({
                                        value: "female",
                                        name: "Female"
                                    });
                                }

                                if (q.Type == 'radio') {
                                    titlemap.push({
                                        value: "yes",
                                        name: "Yes"
                                    });

                                    titlemap.push({
                                        value: "no",
                                        name: "No"
                                    });
                                }

                                var item = {
                                    'field': m,
                                    'label': $translate.instant(q.Label),
                                    'type': q.Type,
                                    'required': q.Required,
                                    'placeholder': $translate.instant(q.Placeholder),
                                    'choices': choices,
                                    'order': q.Order
                                };

                                if (chosenTypes.indexOf(q.Type) > -1) {
                                    var fullkey = m;

                                    if (question == 'RepeatingQuestions') {
                                        fullkey = key + '____' + m;
                                    }

                                    $scope.schema.properties.push({
                                        'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                        'type': schema_type[q.Type],
                                        'order': q.Order,
                                        'fullkey': fullkey,
                                        'key': m,
                                        'formtype': form_type[q.Type],
                                        'placeholder': $translate.instant(q.Placeholder),
                                        'titleMap': titlemap,
                                        'originalType': q.Type
                                    });


                                    $scope.form_items.push({
                                        type: 'fieldset',
                                        htmlClass: 'col-lg-4 col-xs-12',
                                        items: [
                                            {
                                                key: m,
                                                htmlClass: 'pad-left-right',
                                                type: form_type[q.Type],
                                                placeholder: $translate.instant(q.Placeholder),
                                                order: q.Order,
                                                titleMap: titlemap
                                            }
                                        ]
                                    });

                                    $scope.question_items.push(item);
                                } else {

                                    if (q.Type == "repeater" && q.hasOwnProperty('RepeatingQuestions')) {
                                        for (var question1 in tabs[key][question][m]) {
                                            if (tabs[key][question][m].hasOwnProperty(question1) && (question1 == 'Questions' || question1 == 'RepeatingQuestions')) {
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

                                                        var item1 = {
                                                            'field': n,
                                                            'label': $translate.instant(q1.Label),
                                                            'type': q1.Type,
                                                            'required': q1.Required,
                                                            'placeholder': $translate.instant(q1.Placeholder),
                                                            'choices': choices,
                                                            'order': q1.Order
                                                        };

                                                        if (chosenTypes.indexOf(q1.Type) > -1) {
                                                            $scope.schema.properties.push({
                                                                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                'type': schema_type[q1.Type],
                                                                'order': q1.Order,
                                                                'fullkey': m + '____' + n,
                                                                'key': n,
                                                                'formtype': form_type[q1.Type],
                                                                'placeholder': $translate.instant(q1.Placeholder),
                                                                'titleMap': titlemap
                                                            });

                                                            $scope.form_items.push({
                                                                type: 'fieldset',
                                                                htmlClass: 'col-lg-4 col-xs-12',
                                                                items: [
                                                                    {
                                                                        key: n,
                                                                        htmlClass: 'pad-left-right',
                                                                        type: form_type[q1.Type],
                                                                        placeholder: $translate.instant(q1.Placeholder),
                                                                        order: q1.Order,
                                                                        titleMap: titlemap
                                                                    }
                                                                ]
                                                            });

                                                            $scope.question_items.push(item1);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        $scope.model = { filters: [ {} ] };
        $scope.model.filters = _.map(settings.dispatch_field_choice, function (choice) {
            return {
                "field": _.find($scope.schema.properties, function (prop) {
                    return prop.fullkey == choice.field_key;
                })
            };
        });

        hotkeys.bindTo($scope).add({
            combo: 'shift+l',
            description: 'Toggle Incident List',
            callback: function () {
                $log.log('toggle list');
                $scope.toggleList();
            },
            persistent: false
        });

        hotkeys.bindTo($scope).add({
            combo: '+',
            description: 'Zoom in',
            callback: function () {
                $log.log('zooming in');
                if ($scope.map.center.zoom < 18) { $scope.map.center.zoom += 1; }
            },
            persistent: false
        });

        hotkeys.bindTo($scope).add({
            combo: '-',
            description: 'Zoom out',
            callback: function () {
                $log.log('zooming out');
                if ($scope.map.center.zoom > 1) { $scope.map.center.zoom -= 1; }
            },
            persistent: false
        });

        hotkeys.bindTo($scope).add({
            combo: 'return',
            description: 'Add note',
            allowIn: ['INPUT'],
            callback: function (event, hotkey) {
                if (event.target.className.indexOf('note-input') > 0) { $scope.addNote(); }
            },
            persistent: false
        });

        IncidentService.getStatuses().then(function (data) {
//                $log.log(data);
                $scope.status_list = data.map(function (item) {
                    return {
                        key: $translate.instant(item.key),
                        incident_status_id: item.incident_status_id,
                        color: item.color
                    };
                });
            });

        if (questions.DashboardItems && questions.DashboardItems.hasOwnProperty('field_52d47aac9bd13') && questions.DashboardItems.field_52d47aac9bd13 && questions.DashboardItems.field_52d47aac9bd13.hasOwnProperty('RepeatingQuestions') && questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions && questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions.hasOwnProperty('patroller') && questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions.patroller) {
            $scope.assignees = questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions.patroller.Values.map(function (item) {
                for (var i in item) { return { key: i, name: item[i] }; }
            });
        } else {
            $scope.assignees = null;
        }

        var saveUnsavedIncidentInfo = function (unsavedIncident, data) {
            if (unsavedIncident.notes.length > 0) {
                unsavedIncident.notes.forEach(function addNoteForUnsavedIncident(element, index, array) {
                    IncidentService.addNote(data.incident_id, element.field_52ca448dg94ja3, element.field_52ca448dg94ja4)
                        .then(function (data) {  });
                });
            }
            if (unsavedIncident.hasOwnProperty('updatedAssignee')) {
                IncidentService.updateIncident(data.incident_id, {
                        "assigned_to": unsavedIncident.updatedAssignee.assigned_to + ''
                    }
                ).then(function (data) { });
            }
            if (unsavedIncident.hasOwnProperty('updatedStatus')) {
                IncidentService.updateStatus(data.incident_id, {
                        "status_type_id": unsavedIncident.updatedStatus.status_type_id + '',
                        "status_date": unsavedIncident.updatedStatus.status_date,
                        "updated_by": unsavedIncident.updatedStatus.updated_by
                    }
                ).then(function (data) { });
            }
            if (unsavedIncident.hasOwnProperty('updatedLocation')) {
                IncidentService.updateIncident(data.incident_id,
                    unsavedIncident.updatedLocation
                ).then(function (data) {  });
            }

            if (unsavedIncident.hasOwnProperty('incident_data')) {
                IncidentService.updateIncident(data.incident_id,
                    unsavedIncident.incident_data
                ).then(function (data) {  });
            }

            return true
        };

        $scope.$watch('model.filters', function(newValue, oldValue){

            if(update_incident) {

                var prop_data = {};
                var hasData = false;

                for(var i = 0, current_incident = null; i < $scope.incidents.length; ++i) {
                    if($scope.incidents[i].incident_pk != selected_incident_pk)
                        continue;
                    current_incident = $scope.incidents[i];
                    break;
                }

                _.each($scope.model.filters, function (prop) {
                    if (prop.hasOwnProperty('value') && prop.value) {

                        if (prop.field.fullkey.indexOf('____') > 0) {
                            var res = prop.field.fullkey.split("____", 2);

                            if(current_incident.hasOwnProperty(res[0]) && !prop_data.hasOwnProperty(res[0])) {
                                if (current_incident[res[0]].length > 0) {
                                    prop_data[res[0]] = current_incident[res[0]];
                                }
                            }

                            if(prop_data.hasOwnProperty(res[0])){
                                if(prop_data[res[0]].length > 0){
                                    prop_data[res[0]][0][res[1]] = prop.value;
                                }
                                else{
                                    prop_data[res[0]] = [];
                                    var prop_key_value = {};
                                    prop_key_value[res[1]] = prop.value;
                                    prop_data[res[0]].push(prop_key_value);
                                }
                            }
                            else{
                                prop_data[res[0]] = [];
                                var prop_key_value = {};
                                prop_key_value[res[1]] = prop.value;
                                prop_data[res[0]].push(prop_key_value);
                            }

                            try {
                                if(current_incident.hasOwnProperty(res[0])) {
                                    if (current_incident[res[0]].length > 0) {
                                        current_incident[res[0]][0][res[1]] = prop.value;
                                    }
                                    else{
                                        current_incident[res[0]][0][res[1]] = prop.value;
                                    }
                                }
                                else{
                                    current_incident[res[0]][0][res[1]] = prop.value;
                                }

                            }
                            catch(err){
                                var key_value = {};
                                key_value[res[1]] = prop.value;
                                current_incident[res[0]] = [key_value];
                            }
                        } else {
                            prop_data[prop.field.fullkey] = prop.value;
                            current_incident[prop.field.fullkey] = prop.value;
                        }
                        hasData = true;
                    }
                });

                if (hasData) {
                    if ($scope.info.current.hasOwnProperty("incident_id")) {
                        IncidentService.updateIncident($scope.info.current.incident_id,
                            prop_data
                        ).then(function (data) {
                        }, function (error) {
                            growl.error("incident_update_failed");
                        });
                    }
                    else {
                        var incident = null;
                        var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));

                        unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                            if (element.temp_incident_id == $scope.info.current.temp_incident_id) {
                                unsavedIncidents[index]['incident_data'] = prop_data;
                                incident = unsavedIncidents[index];
                                LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                            }
                        });

                        for (var j = 0; j < $scope.incidents.length; j++) {
                            if ($scope.incidents[j].temp_incident_id == incident.temp_incident_id) {
                                $.extend($scope.incidents[j], prop_data);
                            }
                        }
                    }
                }
            }
        }, true);

        var createHeader = function (incident) {
            var response = incident;

            var items = [];
            items.push('#' + incident.incident_pk);

            if (incident.assigned_to) {
                items.push($filter('toTitlecase')(incident.assigned_to.name))
            }

            if (incident.injury) {
                var injury_data = $filter('transformInjuryFirst')(incident.injury);
                if (injury_data && injury_data.trim() != "") {
                    items.push($filter('toTitlecase')(injury_data));
                }
            }
//                    items.push($filter('toElapsedTime')(incident.dt_created, '"mm[m] ss[s]'));
            response['local_dt_created'] = moment.utc(incident.dt_created).tz(tz.name()).format('HH:mm:ss');

            items.push(response['local_dt_created']);
            response['header'] = items.join(", ");
            return response
        };

        var createDummyIncident = function (lat, long, accuracy) {
            var incident_pk = JSON.parse(LS.get('nextIncidentPk'));
            if (!lat) lat = $scope.map.center.lat;
            if (!long) long = $scope.map.center.lng;
            if (!accuracy) accuracy = $scope.map.center.zoom;
            var dummy_incident = {
                "incident_pk": '',
                "location": {
                    "lat": lat,
                    "long": long,
                    "accuracy": accuracy
                },
                "incident_status": [{
                    "color": "ff0000",
                    "key": "call_received",
                    "value": 1
                }],
                "assigned_to": {
                    "name": UserService.currentUser()['name'],
                    "user_id": UserService.currentUser()['user_id']
                },
                "dt_created": moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss'),
                "notes": [],
                "temp_incident_id": $scope.tempIncidentPk
            };
            $scope.tempIncidentPk += 1;
            dummy_incident = createHeader(dummy_incident);
            var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
            if (unsavedIncidents == null) {
                LS.set('unsavedIncidents', JSON.stringify([dummy_incident]));
            }
            else {
                unsavedIncidents.unshift(dummy_incident);
                LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
            }

            $scope.incidents.unshift(dummy_incident);

            $scope.map.markers = $scope.incidents.map(function (incident) {
                var icon = (incident.status == 'closed' || incident.status == 'onscene') ? 'map-user-icon' : 'map-warning-icon';
                return {
                    // group: '',
                    lat: incident.location.lat || parseFloat(currentUser.resorts[0].map_lat),
                    lng: incident.location.long || parseFloat(currentUser.resorts[0].map_lng),
                    icon: urlBase + 'pin_' + incident.incident_status[0].color + '.png',
                    draggable: true
                };

            });
            $scope.relocateMarkers();

            var myLatLng = { lat: $scope.map.markers[0].lat, lng: $scope.map.markers[0].lng };
            var dummy_marker = new google.maps.Marker({
                icon: urlBase + 'pin_' + dummy_incident.incident_status[0].color + '.png',
                position: myLatLng,
                label: incident_pk,
                draggable: true,
            });
            dummy_marker.incident = dummy_incident;
            google.maps.event.addListener(dummy_marker, 'click', function() {
                $scope.highlight(this.incident);
            });

            google.maps.event.addListener(dummy_marker, 'dragend', function(point) {
                IncidentService.updateIncident(this.incident.incident_id, {
                        "field_52ca456962ba8": {
                            lat: point.latLng.lat(),
                            long: point.latLng.lng()
                        }
                    }).then(function (data) {
                            growl.info("Incident location updated");
                        }, function (error) {
                            growl.error("incident_update_failed");
                    });
            });
            $scope.googleMapMarkers.unshift(dummy_marker);
            dummy_marker.setMap($scope.googleMap);
            return dummy_incident
        };

        $scope.list = {
            dateFrom: start,
            dateTo: end,

            add: function (lat, long, accuracy) {
                growl.info('ADDING_INCIDENT');

                list_incidents = false;

                var incident = createDummyIncident(lat, long, accuracy);

                $scope.highlight(incident);

                if (typeof(lat) === undefined) lat = incident.location.lat;
                if (typeof(long) === undefined) long = incident.location.long;
                if (typeof(accuracy) === undefined) accuracy = incident.location.accuracy;
                var default_data = {
                    "field_52ca456962ba8": {
                        "lat": lat,
                        "long": long,
                        "accuracy": accuracy
                    }
                };

                $.extend(default_data, defaults);

                IncidentService.createIncident(default_data).then(function (data) {
                    growl.info('INCIDENT_ADDED');

                    var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));

                    unsavedIncidents.forEach(function updateIncidentIdUnsavedIncident(element, index, array) {
                        if (element.temp_incident_id == incident.temp_incident_id) {
                            var status = saveUnsavedIncidentInfo(element, data);
                            unsavedIncidents[index]['incident_id'] = data.incident_id;
                            unsavedIncidents[index]['incident_pk'] = data.incident_pk;
                            unsavedIncidents[index] = createHeader(unsavedIncidents[index]);
                            LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                            var marker = $scope.findMarker(unsavedIncidents[index]);
                            marker.setLabel('#' + data.incident_pk.toString());
                        }
                    });

                    $scope.incidents.forEach(function updateIncidentIdLive(element, index, array) {
                        if (element.hasOwnProperty('temp_incident_id')) {
                            if (element.temp_incident_id == incident.temp_incident_id) {
                                $scope.incidents[index]['incident_id'] = data.incident_id;
                                $scope.incidents[index]['incident_pk'] = data.incident_pk;
                                $scope.incidents[index] = createHeader($scope.incidents[index]);
                            }
                        }
                    });
                    $scope.incidentToHighlight = data.incident_id;
                    selected_incident_pk = data.incident_pk;
                    list_incidents = true;

                }, function (reason) {
                    list_incidents = true;
                });
                $scope.init();
            }
        };

        var divIcon = function (icon, text, color) {
            return {
                type: 'div',
                iconSize: [30, 108],
//                iconAnchor: [31, 101],
//                popupAnchor: [55, -200],
                html: '<div class><svg height="50" width="45">' +
                '<path d="m3.03343,0.18326c0.01996,0.09996 -0.39914,0.38318 -0.93798,0.63308c-0.89807,0.4165 -1.17747,0.71639 -1.9558,2.0492c-0.21953,0.38318 -0.21953,26.2064 0,26.58958c0.77833,1.36613 1.03777,1.63269 2.01567,2.06586l1.01781,0.46649l6.12683,0.03332l6.14679,0.04998l0.11974,1.24951c0.1397,1.29949 0.57876,3.89847 1.05773,6.33085c0.73841,3.66523 0.87812,4.265 0.99786,4.49824c0.05987,0.13327 0.19957,0.69972 0.31931,1.24951c0.31931,1.63269 0.73841,3.48197 0.87811,3.78186c0.05988,0.1666 0.15966,0.4165 0.21953,0.5831c0.07983,0.18326 0.2794,0 0.65859,-0.63309c0.29935,-0.4998 0.57876,-0.93297 0.63862,-0.98294c0.05987,-0.04997 0.39914,-0.56645 0.77833,-1.1662c0.35923,-0.59977 1.1176,-1.7993 1.65644,-2.66563c0.5588,-0.86633 1.69636,-2.7156 2.53455,-4.08173c0.81824,-1.38279 1.55665,-2.53234 1.61652,-2.58232c0.05987,-0.04998 0.71846,-1.13289 1.45687,-2.41573c0.75837,-1.28283 1.49678,-2.51567 1.63648,-2.74892l0.2794,-0.4165l5.54807,-0.0833c5.28864,-0.08331 5.58799,-0.09996 6.48606,-0.46649c0.93799,-0.38318 1.75623,-1.21619 1.75623,-1.78263c0,-0.14994 0.17962,-0.31654 0.39915,-0.36653c0.39914,-0.0833 0.39914,-0.23324 0.39914,-13.31145c0,-9.57958 -0.05987,-13.21149 -0.21953,-13.19483c-0.11974,0.03332 -0.45901,-0.31654 -0.75837,-0.74971c-0.53884,-0.81635 -1.43691,-1.44943 -2.07554,-1.44943c-0.21953,0 -0.4191,-0.14994 -0.47897,-0.3332c-0.09978,-0.3332 -0.27939,-0.3332 -19.23865,-0.3332c-13.89015,0 -19.11891,0.04998 -19.079,0.18326z" id="svg_2" fill="#' + color + '"/>' +
                '<text xml:space="preserve" font-weight="bold" text-anchor="middle" font-family="Sans-serif" font-size="14" id="svg_1" y="20.70196" x="23.50113" stroke-linecap="null" stroke-linejoin="null" stroke-dasharray="null" stroke-width="0" fill="#000000">#' + text + '</text>' +
                '</svg></div>'
            };
        };

        $scope.map = {
            initialized: false,
            defaults: {
                //scrollWheelZoom: false,
                //doubleClickZoom:false,
                trackResize: true,
                pan: {
                    animate: true,
                    duration: 0.85,
                    easeLinearity: 0.3
                },
                maxZoom: 21
            },
            center: {
                lat: 70.00,
                lng: 35.00,
                zoom: 3
            },
            markers: [],
            layers: {
                baselayers: {
                    googleRoadmap: {
                        name: 'Map',
                        layerType: 'ROADMAP',
                        type: 'google'
                    },
                    googleTerrain: {
                        name: 'Terrain',
                        layerType: 'TERRAIN',
                        type: 'google'
                    },
                    googleHybrid: {
                        name: 'Satellite',
                        layerType: 'HYBRID',
                        type: 'google'
                    }
                }
            }
        };

        var timer = null;
        $scope.toggleList = function () { $scope.mapNotToggle = !$scope.mapNotToggle; };
        $scope.init = function () {
            if (list_incidents) {
                growl.info('LOADING_INCIDENTS');
                IncidentService.fetchMap(start, end, resort_id, 0, 1).then(function (data) {
                    var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
                    if (unsavedIncidents != null && unsavedIncidents.length > 0) {
                        var items = [];
                        data.results.forEach(function createListOfIncidentId(element, index, array) {
                            items.push(element.incident_pk);
                        });
                        unsavedIncidents.forEach(function removeSyncedIncidents(element, index, array) {
                            if (items.indexOf(element.incident_pk) != -1) {
                                unsavedIncidents.splice(index, 1);
                            }
                        });
                        LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                    }
                    $scope.incidents = data.results.map(function (incident) { return createHeader(incident); });
                    if (unsavedIncidents != null) {
                        if (unsavedIncidents.length > 0) $scope.incidents = unsavedIncidents.concat($scope.incidents);
                    }
                    $scope.map.markers = $scope.incidents.map(function (incident) {
                        var icon = (incident.status == 'closed' || incident.status == 'onscene') ? 'map-user-icon' : 'map-warning-icon';
                        return {
                            // group: '',
                            lat: incident.location.lat || parseFloat(currentUser.resorts[0].map_lat),
                            lng: incident.location.long || parseFloat(currentUser.resorts[0].map_lng),
                            icon: urlBase + 'pin_' + incident.incident_status[0].color + '.png',
                            draggable: true,
                            incident: incident
//                        icon: divIcon(icon, $filter('toElapsedTime')(incident.dt_created, "mm:ss"))
                        };
                    });

                    if ($scope.info.current == null && !($scope.map.initialized)) {

                        if (currentUser.resorts[0].map_lat && currentUser.resorts[0].map_lng) {
                            $scope.map.center.lat = parseFloat(currentUser.resorts[0].map_lat);
                            $scope.map.center.lng = parseFloat(currentUser.resorts[0].map_lng);

//                        $log.log($scope.map.center);

                        } else {
                            if ($scope.incidents.length > 0) {
                                $scope.highlight($scope.incidents[0]);
                            }
                        }
                        $scope.map.center.zoom = settings.initial_map_zoom_level;
                        $scope.map.initialized = true;
                        $scope.initMap(true);
                    }
                });
            }
            $timeout.cancel(timer);
            timer = $timeout($scope.init, 15000);
        };
        $scope.$on( "$destroy", function (event) { $timeout.cancel(timer); } );
        $scope.getMarker = function (incident) {
            var icon = (incident.status == 'closed' || incident.status == 'onscene') ? 'map-user-icon' : 'map-warning-icon';
            return {
                // group: '',
                lat: incident.location.lat || parseFloat(currentUser.resorts[0].map_lat),
                lng: incident.location.long || parseFloat(currentUser.resorts[0].map_lng),
                    icon: urlBase + 'pin_' + incident.incident_status[0].color + '.png',
                draggable: true
//                icon: divIcon(icon, incident.dt_created)
            };
        };
        $scope.info = {
            isOpen: false,
            current: null,
            note: null,
            notes: null
        };
        $scope.addNote = function () {
            if ($scope.info.note && $scope.info.note.length > 0) {
                growl.info('SAVING_NOTE');

                var time = moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss');

                if ($scope.info.current.hasOwnProperty("incident_id")) {
                    IncidentService.addNote($scope.info.current.incident_id, $scope.info.note, time).then(function (data) {
                        growl.info('NOTE_SAVED');

                        if (!$scope.info.current.hasOwnProperty('notes') || $scope.info.current.notes == null || $scope.info.current.notes == undefined) {
                            $scope.info.current.notes = [];
                        }


                        data.field_52ca448dg94ja4 = moment.utc(data.field_52ca448dg94ja4).tz(tz.name()).format($scope.datetime_format);

                        $scope.info.current.notes.unshift(data);

                        $scope.info.note = null;
                    });
                }
                else {
                    var data = {
                        "field_52ca448dg94ja3": $scope.info.note,
                        "field_52ca448dg94ja4": time
                    };
                    var incident = null;
                    var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
                    unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                        if (element.temp_incident_id == $scope.info.current.temp_incident_id) {
                            unsavedIncidents[index]['notes'].unshift(data);
                            incident = unsavedIncidents[index];
                            LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                        }
                    });
                    data.field_52ca448dg94ja4 = moment.utc(data.field_52ca448dg94ja4).tz(tz.name()).format($scope.datetime_format);

                    for (var j = 0; j < $scope.incidents.length; j++) {
                        if ($scope.incidents[j].temp_incident_id == incident.temp_incident_id) {
                            $scope.incidents[j].notes.unshift(data)
                        }
                    }

                    $scope.info.note = null;
                }
            }
        };

        $scope.updateStatus = function () {
            var statusColor = null;
            var statusName = null;
            for (var i = 0; i < $scope.status_list.length; i++) {
                if ($scope.status_list[i].incident_status_id == $scope.incident_status) {
                    statusColor = $scope.status_list[i].color;
                    statusName = $scope.status_list[i].key;
                }
            }
            if ($scope.incident_status) {
                // if deleted, get confirmation
                if ($scope.incident_status == 9) {
                    var modalInstance = $modal.open({
                        animation: true,
                        templateUrl: '/app/templates/incidents/confirm.html',
                        controller: 'ConfirmModalCtrl',
                        size: 'md'
                    });

                    modalInstance.result.then(function (is_allowed) {

                        if ($scope.info.current.hasOwnProperty("incident_id")) {
                            for (var j = 0; j < $scope.incidents.length; j++) {
                                if ($scope.incidents[j].incident_id == $scope.info.current.incident_id) {
                                    $scope.incidents[j]['incident_status'][0]['color'] = statusColor;
                                    $scope.incidents[j]['incident_status'][0]['key'] = statusName;
                                    $scope.incidents[j]['incident_status'][0]['value'] = $scope.incident_status;
                                }
                            }
                            var marker = $scope.googleMapMarkers.find(function(row){
                            });
                            IncidentService.updateStatus($scope.info.current.incident_id, {
                                    "status_type_id": $scope.incident_status + '',
                                    "status_date": moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss'),
                                    "updated_by": currentUser.user_id
                                }
                            ).then(function (data) {
                                    growl.info("Status updated");
                                    $scope.init();
                                    $scope.info.isOpen = false;
                                });
                        }
                        else {
                            var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
                            var incident = null;
                            unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                                if (element.temp_incident_id == $scope.info.current.temp_incident_id) {
                                    unsavedIncidents[index]['updatedStatus'] = {
                                        "status_type_id": $scope.incident_status + '',
                                        "status_date": moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss'),
                                        "updated_by": currentUser.user_id
                                    };
                                    unsavedIncidents[index]['incident_status'][0]['color'] = statusColor;
                                    unsavedIncidents[index]['incident_status'][0]['key'] = statusName;
                                    unsavedIncidents[index]['incident_status'][0]['value'] = $scope.incident_status;

                                    incident = unsavedIncidents[index];

                                    for (var j = 0; j < $scope.incidents.length; j++) {
                                        if ($scope.incidents[j].temp_incident_id == incident.temp_incident_id) {
                                            $scope.incidents[j] = incident
                                        }
                                    }
                                    LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                                }
                            });
                        }

                    }, function () {
                        $log.info('Modal dismissed at: ' + new Date());
                    });
                } else {
                    // else update status directly
                    if ($scope.info.current.hasOwnProperty("incident_id")) {
                        var marker = $scope.googleMapMarkers.find(function(row){
                            return $scope.info.current.incident_id == row.incident.incident_id;
                        });
                        var pinColor = statusColor === 'ffff' ? 'cccccc' : statusColor;
                        marker.setIcon(urlBase + 'pin_' + pinColor + '.png');
                        marker.incident.incident_status[0].color = statusColor;
                        marker.incident.incident_status[0].key = statusName;
                        marker.incident.incident_status[0].value = $scope.incident_status;
                        for (var j = 0; j < $scope.incidents.length; j++) {
                            if ($scope.incidents[j].incident_id == $scope.info.current.incident_id) {
                                $scope.incidents[j]['incident_status'][0]['color'] = statusColor;
                                $scope.incidents[j]['incident_status'][0]['key'] = statusName;
                                $scope.incidents[j]['incident_status'][0]['value'] = $scope.incident_status;
                            }
                        }
                        IncidentService.updateStatus($scope.info.current.incident_id, {
                                "status_type_id": $scope.incident_status + '',
                                "status_date": moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss'),
                                "updated_by": currentUser.user_id
                            }
                        ).then(function (data) {
                                growl.info("Status updated");
                            });
                    }
                    else {
                        var incident = null;
                        var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
                        unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                            if (element.incident_pk == $scope.info.current.incident_pk) {
                                unsavedIncidents[index]['updatedStatus'] = {
                                    "status_type_id": $scope.incident_status + '',
                                    "status_date": moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss'),
                                    "updated_by": currentUser.user_id
                                };

                                unsavedIncidents[index]['incident_status'][0]['color'] = statusColor;
                                unsavedIncidents[index]['incident_status'][0]['key'] = statusName;
                                unsavedIncidents[index]['incident_status'][0]['value'] = $scope.incident_status;

                                incident = unsavedIncidents[index];

                                for (var j = 0; j < $scope.incidents.length; j++) {
                                    if ($scope.incidents[j].temp_incident_id == incident.temp_incident_id) {
                                        $scope.incidents[j] = incident
                                    }
                                }
                                LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                            }
                        });
                    }
                }
            }
        };

        $scope.updateAssignee = function () {
            var assigneeName = null;
            for (var i = 0; i < $scope.assignees.length; i++) {
                if ($scope.assignees[i]['key'] == $scope.assigned_to) {
                    assigneeName = $scope.assignees[i]['name'];
                    break;
                }
            }

            if ($scope.assigned_to) {
                if ($scope.info.current.hasOwnProperty("incident_id")) {
                    for (var j = 0; j < $scope.incidents.length; j++) {
                        if ($scope.incidents[j].incident_id == $scope.info.current.incident_id) {
                            $scope.incidents[j]['assigned_to']['user_id'] = $scope.assigned_to;
                            $scope.incidents[j]['assigned_to']['name'] = assigneeName;
                            $scope.incidents[j] = createHeader($scope.incidents[j]);
                        }
                    }
                    IncidentService.updateIncident($scope.info.current.incident_id, {
                            "assigned_to": $scope.assigned_to + ''
                        }
                    ).then(function (data) {
                            growl.info("Assignee updated");
                        });
                }
                else {
                    var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));
                    var incident = null;
                    unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                        if (element.incident_pk == $scope.info.current.incident_pk) {
                            unsavedIncidents[index]['updatedAssignee'] = {
                                "assigned_to": $scope.assigned_to + ''
                            };
                            unsavedIncidents[index]['assigned_to']['user_id'] = $scope.assigned_to + '';
                            unsavedIncidents[index]['assigned_to']['name'] = assigneeName;

                            unsavedIncidents[index] = createHeader(unsavedIncidents[index]);
                            incident = unsavedIncidents[index];

                            for (var j = 0; j < $scope.incidents.length; j++) {
                                if ($scope.incidents[j].temp_incident_id == incident.temp_incident_id) {
                                    $scope.incidents[j] = incident
                                }
                            }
                            LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                        }
                    });
                }
            }
        };

        $scope.highlight = function (incident) {
//            $log.log(incident);
            $scope.info.isOpen = false;
            angular.forEach($scope.incidents, function (incident) {
                incident.selected = false;
            });

            incident.selected = true;
            selected_incident_pk = incident.incident_pk;

            var incidentMarker = $scope.getIncidentFromRelocatedMarker(incident);
            $scope.map.center.lat = parseFloat(incidentMarker.lat) || parseFloat(currentUser.resorts[0].map_lat);
            $scope.map.center.lng = parseFloat(incidentMarker.lng) || parseFloat(currentUser.resorts[0].map_lng);

            $scope.googleMap.setCenter(incidentMarker);
//            $scope.map.center.zoom = 16; //incident.zoom;

//            $scope.info.isOpen = false;

            $scope.info.current = incident;
//            $scope.info.current.datetime = incident.datetime.toLocaleString().replace('at ', '');
            if (!incident.hasOwnProperty('notes')) {
                $scope.info.current.notes = [];
            }

            $scope.incident_status = $scope.info.current.incident_status[0].value;
            $scope.incident_status = $scope.info.current.incident_status[0].value;
            $scope.assigned_to = $scope.info.current.assigned_to.user_id;
            update_incident = false;

            $scope.model.filters.map(function(currentValue, index){
                if (!currentValue) return;
                if (!currentValue.field) return;
                if (!currentValue.field.fullkey) return;
                if (currentValue.field.fullkey.indexOf('____') > 0) {
                    var res = currentValue.field.fullkey.split("____", 2);
                    try {
                        $scope.model.filters[index].value = incident[res[0]][0][res[1]];
                    }
                    catch(err) {
                        $scope.model.filters[index].value = "";
                    }
                }
                else {
                    $scope.model.filters[index].value = incident[currentValue.field.key];
                }
            });

            setTimeout(function(){ update_incident = true; }, 200);

            if ($scope.info.current.hasOwnProperty("incident_id")) {
                growl.info('LOADING_NOTES');
                IncidentService.fetchNotes($scope.info.current.incident_id).then(function (response) {

                    $scope.info.current.notes = [];
//                $log.log(response);

                    angular.forEach(response.results, function (value, key) {
                        $scope.info.current.notes.push({
                            field_52ca448dg94ja3: value.field_52ca448dg94ja3,
                            field_52ca448dg94ja4: moment.utc(value.field_52ca448dg94ja4).tz(tz.name()).format($scope.datetime_format),
                            field_52ca448dg94ja5: value.field_52ca448dg94ja5,
                            note_id: value.note_id
                        });
                    });
//                $scope.info.current.notes = response.results;
                });
            }

            $scope.info.isOpen = true;
        };

        $scope.saveUnsavedIncidentRefresh = function () {
            var unsavedIncidents = JSON.parse(LS.get('unsavedIncidents'));

            if (unsavedIncidents != null && unsavedIncidents.length > 0) {

                unsavedIncidents.forEach(function saveEachIncident(unsavedElement, index, array) {
                    IncidentService.createIncident({
                        "field_52ca456962ba8": {
                            "lat": unsavedElement.location.lat,
                            "long": unsavedElement.location.long,
                            "accuracy": unsavedElement.location.accuracy
                        }
                    }).then(function (data) {
                        unsavedIncidents.forEach(function removeArrayElement(element, index, array) {
                            if (element.incident_pk == unsavedElement.incident_pk) {
                                var status = saveUnsavedIncidentInfo(element, data);
                                unsavedIncidents.splice(index, 1);
                                LS.set('unsavedIncidents', JSON.stringify(unsavedIncidents));
                            }
                        });

                    }, function (reason) {

                    });
                });

                $scope.init();

            }
            return true
        };

        // var syncStatus = $scope.saveUnsavedIncidentRefresh();

    
}]);
