'use strict';


angular.module('app')
    .controller('LocationEditCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, LocationService, AreaService, currentUser, growl, leafletData, $http, hotkeys) {
        var id = $stateParams.locationId;

        var style_lifts = {
            "color": "#ff0000",
            "dashArray": "15,5",
            "weight": "3"
        };
        var style_buildings = {
            "color": "#0000ff",
            "weight": "1"
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

        var resort_id = currentUser.resorts[0].resort_id;

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
                }
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

        //{"resort_count":1,"user_id":"397db175-1c28-4385-86f9-bcdc5bbf03ff","name":"Mr Manager","phone":"0138562894","role_id":[{"value":3,"key":"manager"}],"resorts":[{"resort_logo":"","map_kml":"http://api.medic52.local/static/content/cf597e6b-25f9-4fa9-8def-2790e1ef2dac/perisher.kml_shUkArB.json","report_form":"","resort_id":"cf597e6b-25f9-4fa9-8def-2790e1ef2dac","resort_name":"Perisher","map_type":{"value":1,"key":"Google Map"},"map_lat":-36.404471,"map_lng":148.413887,"unit_format":{"value":1,"key":"Metric"},"timezone":"Australia/Sydney","datetime_format":{"value":1,"key":"dd/mm/yyyy hh:mm:ss"},"resort_controlled_substances":true,"resort_asset_management":true}],"token":"9984026d011949e045b2a1ff3138ac698674e7c0","user_connected":{"value":1,"key":"network"},"user_controlled_substances":true,"user_asset_management":true,"email":"manager@perisherski.com","role":"Manager","isManager":true}

        if (!($scope.map.initialized)) {
            if (currentUser && currentUser.resorts.length > 0 && currentUser.resorts[0].map_kml) {
                leafletData.getMap().then(function (map) {

                    $http.get(currentUser.resorts[0].map_kml).success(function (data) {

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
                });
            }

            $scope.map.center.zoom = 18;
            $scope.map.initialized = true;
        }

        hotkeys.bindTo($scope).add({
            combo: '+',
            description: 'Zoom in',
            callback: function () {
                $log.log('zooming in');

                if ($scope.map.center.zoom < 18) {
                    $scope.map.center.zoom += 1;

                    leafletData.getMap().then(function (map) {
                        map.setZoom($scope.map.center.zoom);
                    });

                }
            },
            persistent: false
        });

        hotkeys.bindTo($scope).add({
            combo: '-',
            description: 'Zoom out',
            callback: function () {
                $log.log('zooming out');

                if ($scope.map.center.zoom > 1) {
                    $scope.map.center.zoom -= 1;

                    leafletData.getMap().then(function (map) {
                        map.setZoom($scope.map.center.zoom);
                    });
                }
            },
            persistent: false
        });

        AreaService.fetchAll(1000, 0, '', 'area_name', 'asc')
            .then(function (data) {
                $scope.areas = data.results;
            },
            function (error) {
                growl.error(error.detail);
            }
        )
            .finally(function () {
                //$scope.location.area_id = $scope.areas[0].area_id;
            });


        $scope.get = function () {
            if (id) {
                growl.info("LOADING_LOCATION");
                LocationService.fetch(id).then(function (data) {
                        $scope.location = data;

                        if ($scope.location.area) {
                            $scope.location.area_id = $scope.location.area.area_id;
                        }

                        if (data.map_lat && data.map_long) {
                            $scope.map.center.lat = data.map_lat;
                            $scope.map.center.lng = data.map_long;

                            $scope.map.markers = [{
                                lat: $scope.map.center.lat,
                                lng: $scope.map.center.lng,
                                draggable: true
                            }];
                        }

                        $scope.$on('leafletDirectiveMarker.dragend', function (e, args) {
                            $scope.location.map_lat = Math.round(parseFloat(args.leafletEvent.target._latlng.lat) * 10000) / 10000;
                            $scope.location.map_long = Math.round(parseFloat(args.leafletEvent.target._latlng.lng) * 10000) / 10000;

                            $scope.map.center.lat = $scope.location.map_lat;
                            $scope.map.center.lng = $scope.location.map_long;
                        });

                        $scope.$watch('location.map_lat', function (newValue, oldValue) {
                            if (newValue && newValue != oldValue) {
                                var map_lat = Math.round(parseFloat(newValue) * 10000) / 10000;
                                $scope.map.markers[0].lat = map_lat;
                                $scope.map.center.lat = map_lat;
                            }
                        });

                        $scope.$watch('location.map_long', function (newValue, oldValue) {
                            if (newValue && newValue != oldValue) {
                                var map_long = Math.round(parseFloat(newValue) * 10000) / 10000;
                                $scope.map.markers[0].lng = map_long;
                                $scope.map.center.lng = map_long;
                            }
                        });

                    },
                    function (error) {
                        growl.info(error.detail);
                    }
                );
            }
        };

        $scope.update = function () {
            if (id) {
                growl.info("UPDATE_LOCATION");
                LocationService.update(id, $scope.location.location_name, $scope.location.area_id, $scope.location.map_lat, $scope.location.map_long).then(function (data) {
//                        $log.log(data);
                        growl.success("location_updated_successfully");
                    },
                    function (error) {
                        growl.info(error.detail);
                    });
            }
        };

    });
