'use strict';

angular.module('app')
    .controller('HeatmapCtrl', function ($scope, $rootScope, $state, $location, $timeout, $log, $filter, $intercom, UserService, currentUser, IncidentService, growl, leafletData, DateRangeService, $http, settings) {

        var style_lifts = {
            "color": "#ff0000",
            "dashArray": "15,5",
            "weight": "3"
        };
        var style_buildings = {
            "color": "#0000ff",
            "weight": "1"
        };
        var style_red = {
            "color": "#ff0000",
            "weight": "3"
        };
        var style_green = {
            "color": "#00ff00",
            "weight": "3"
        };
        var style_blue = {
            "color": "#0000ff",
            "weight": "3"
        };
        var style_doubleblue = {
            "color": "#0000ff",
            "dashArray": "15,10,1,10,1,10",
            "weight": "3"
        };
        var style_black = {
            "color": "#000000",
            "weight": "3"
        };
        var style_doubleblack = {
            "color": "#000000",
            "dashArray": "15,10,1,10,1,10",
            "weight": "3"
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
            dashboard_feature_last_used: "Heatmap"
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

        function toUTC(value) {
            return moment(value, 'YYYY-MM-DD HH:mm:ss').tz(tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format($scope.datetime_format);
        }

        var diff = new Date(current.getTime() - (7 * 24 * 60 * 60 * 1000));
        var tzDate = moment(current).utc().format('YYYY-MM-DD');
        //var start = tzDate + ' 00:00:00';
        var end = tzDate + ' 23:59:59';

        var resort = currentUser.resorts[0];
        var resort_id = resort.resort_id;
        $scope.list = DateRangeService.range;

        $scope.mapLoaded = false;

        var divIcon = function (icon, text) {
            return {
                type: 'div',
                iconSize: [200, 0],
                iconAnchor: [22, 94],
                popupAnchor: [55, -200],
                html: '<div class="' + icon + '\"><span><i></i><strong>' + text + '</strong></span></div>'
            };
        };

        $scope.map = {
            initialized:false,
            defaults: {
//                scrollWheelZoom: false,
                trackResize: true,
                pan: {
                    animate: true,
                    duration: 0.85,
                    easeLinearity: 0.3
                }
            },
            center: {
                lat: resort.map_lat,
                lng: resort.map_lng,
                zoom: 16
            },
            markers: {},
            layers: {
                baselayers: {
                    osm: {
                        name: 'OpenStreetMap',
                        layerType: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        type: 'xyz'
                    },
                    // googleRoadmap: {
                    //     name: 'Google Streets',
                    //     layerType: 'ROADMAP',
                    //     type: 'google'
                    // },
                    // googleTerrain: {
                    //     name: 'Google Terrain',
                    //     layerType: 'TERRAIN',
                    //     type: 'google'
                    // },
                    // googleHybrid: {
                    //     name: 'Google Hybrid',
                    //     layerType: 'HYBRID',
                    //     type: 'google'
                    // }
                },
                "overlays": {}
            }
        };

        var heatmap = new L.heatLayer([],{radius:25, maxZoom:18, minOpacity:0.25});

        leafletData.getMap().then(function (map) {
            map.addLayer(heatmap);

            if (currentUser && currentUser.resorts.length > 0 && currentUser.resorts[0].map_kml) {

                $http.get(settings.map_kml).success(function (data) {

                    function onEachFeature(feature, layer) {
                        var popupContent = feature.properties.description;
                        var popupTitle = feature.properties.name;

                        if (feature.properties && feature.properties.popupContent) {
                            popupContent += feature.properties.popupContent;
                        }
                        layer.bindPopup(popupContent);
                    }

                    // add buildings
                    L.geoJson(data.buildings, {
                        style: function (feature) {
                            if (data.hasOwnProperty('style_buildings')) {
                                return data.style_buildings;
                            } else {
                                return style_buildings;
                            }
                        },
                        onEachFeature: onEachFeature
                    }).addTo(map);


                    // add runs
                    L.geoJson(data.runs, {
                        style: function (feature) {
                            switch (feature.properties.rating) {
                                case 'red':
                                    if (data.hasOwnProperty('style_red')) {
                                        return data.style_red;
                                    } else {
                                        return style_red; // Easiest / red
                                    }
                                case 'green':
                                    if (data.hasOwnProperty('style_green')) {
                                        return data.style_green;
                                    } else {
                                        return style_green; // Easiest / Green
                                    }
                                case 'blue':
                                    if (data.hasOwnProperty('style_blue')) {
                                        return data.style_blue;
                                    } else {
                                        return style_blue; // Difficult / Blue
                                    }
                                case 'doubleblue':
                                    if (data.hasOwnProperty('style_doubleblue')) {
                                        return data.style_doubleblue;
                                    } else {
                                        return style_doubleblue; // More Difficult / Double Blue
                                    }
                                case 'black':
                                    if (data.hasOwnProperty('style_black')) {
                                        return data.style_black;
                                    } else {
                                        return style_black; // Most Difficult / Black
                                    }
                                case 'doubleblack':
                                    if (data.hasOwnProperty('style_doubleblack')) {
                                        return data.style_doubleblack;
                                    } else {
                                        return style_doubleblack;
                                    }
                            }
                        },
                        onEachFeature: onEachFeature
                    }).addTo(map);

                    // add lifts
                    L.geoJson(data.lifts, {
                        style: function (feature) {
                            if (data.hasOwnProperty('style_lifts')) {
                                return data.style_lifts;
                            } else {
                                return style_lifts;
                            }
                        },
                        onEachFeature: onEachFeature
                    }).addTo(map);


                });
            }
        });

        var timer = null;

        $scope.init = function () {
            growl.info('LOADING_INCIDENTS');
            var start_time = toUTC(moment($scope.list.dateFrom).format('YYYY-MM-DD 00:00:00'));
            var end_time = toUTC(moment($scope.list.dateTo).format('YYYY-MM-DD 23:59:59'));

            IncidentService.fetchAll(start_time, end_time, resort_id, 2000, 1).then(function (data) {
                $scope.loading = false;

                $scope.incidents = data.results;

                leafletData.getMap().then(function (map) {
                    if ($scope.incidents) {
                        var dataPoints = $scope.incidents.map(function (incident) {
                            return [
                                incident.location.lat,
                                incident.location.long,
                                0.2
                            ];
                        });

                        heatmap.setLatLngs(dataPoints);
                        heatmap.redraw();
                    }
                });


                if (!$scope.mapLoaded) {
                    $scope.mapLoaded=true;

                    //$scope.highlight($scope.incidents[0]);
                    $scope.map.center.zoom = settings.initial_map_zoom_level;
                }
            });

            timer = $timeout($scope.init, 15000);

            $scope.$on(
                "$destroy",
                function (event) {

                    $timeout.cancel(timer);

                }
            );
        };

        $scope.getMarker = function (incident) {
            var icon = (incident.status == 'closed' || incident.status == 'onscene') ? 'map-user-icon' : 'map-warning-icon';

            return {
                lat: incident.lat,
                lng: incident.lng,
                icon: divIcon(icon, incident.time_started)

            };
        };

        $scope.info = {
            isOpen: false,
            current: null,
            note: null,
            notes: null
        };

//        $scope.addNote = function () {
//            if ($scope.info.note.length > 0) {
//                growl.info('SAVING_NOTE');
//                IncidentService.saveNote($scope.info.current.id, '', $scope.info.note).then(function (data) {
////                    $log.log(data);
//
//                    growl.info('NOTE_SAVED');
//                    var timenow = new Date();
//                    var time = timenow.getHours() + ":" + timenow.getMinutes();
//                    $scope.info.current.notes.push({message: $scope.info.note, time: time});
//                    $scope.info.note = null;
//                });
//            }
//        };

//        $scope.$on('leafletDirectiveMarker.click', function (e, args) {
////            console.log(args);
//            var id = parseInt(args.markerName)
//            $scope.highlight($scope.incidents[id]);
//            $scope.info.isOpen = true;
//        });
//
//        $scope.$on('leafletDirectiveMap.click', function (e, args) {
//            $scope.info.isOpen = false;
//        });
//
        $scope.highlight = function (incident) {
//            $log.log(incident);
            $scope.map.center.lat = incident.location.lat;
            $scope.map.center.lng = incident.location.long;
//          $scope.map.center.zoom = 16; //incident.zoom;

//            $scope.info.isOpen = false;

            $scope.info.current = incident;
            $scope.info.current.notes = [];
        };

    });