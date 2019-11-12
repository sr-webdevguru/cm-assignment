'use strict';

angular.module('schemaForm')
    .run(['$templateCache',
        function ($templateCache) {
            var schemaHtml =
                '<div  class="form-group" ng-class="{\'has-success\': hasSuccess()}"' +
                '   googlemap                                                      ' +
                '   ng-show="form.key"                                             ' +
                '   schema-validate="form"                                         ' +
                '   ng-model="$$value$$">                                          ' +
                '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +
                '   <div>' +
                '       <input class="form-control"/>' +
                '   </div>' +
                '   <div style="min-height: 45px;text-align: right;">' +
                '       <button type="button" class="btn btn-primary" style="margin: 10px 0px;" ng-click="openModal()">[["large_view"|translate]]</button>' +
                '   </div>' +
                '   <div style="min-height: 525px;"><div class="map" width="100%" style="min-height: 525px;margin: 0px;padding: 0px"></div></div>' +
                '</div>';

            $templateCache.put('googlemap.html', schemaHtml);
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var googlemap = function (name, schema, options) {
                if (schema.type === 'googlemap'
                    && schema.format === 'object') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'googlemap';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(googlemap);

            schemaFormDecoratorsProvider.addMapping(
                'bootstrapDecorator',
                'googlemap',
                'googlemap.html'
            );

            schemaFormDecoratorsProvider.createDirective(
                'googlemap',
                'googlemap.html'
            );
        }])
    .directive('googlemap',
    ['googlemapModalService', '$http', 'UserService','hotkeys', function (googlemapModalService, $http, UserService, hotkeys) {
        return {
            restrict: 'A',
            require: 'ngModel',

            link: function (scope, element, attrs, ngModel) {
                var map,
                    marker,
                    geocoder,
                    input,
                    zoom = 16,
                    defLoc = {
                        lat: -25.363882,
                        lng: 131.044922,
                        zoom: 16
                    };

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

                var once = scope.$watch('ngModel.$viewValue', function (value) {
                    if (value) {
                        setMap();
                        once();
                    }
                });

                function setMap() {
                    // Update values to map
                    if (ngModel.$modelValue !== undefined) {
                        var model = ngModel.$modelValue;

                        var lat = 0.0;
                        var long = 0.0;
                        var accuracy = 16;

                        if (model && model.hasOwnProperty('lat')) {
                            lat = model.lat;
                        }

                        if (model && model.hasOwnProperty('long')) {
                            long = model.long;
                        }

                        if (model && model.hasOwnProperty('accuracy')) {
                            accuracy = model.accuracy;
                        }

                        defLoc = {
                            lat: lat,
                            lng: long,
                            accuracy: accuracy
                        };

                        //zoom = accuracy;

                        placeMarker(defLoc, true);
                        map.setZoom(defLoc.accuracy);
                        map.panTo(defLoc);
                    }
                }

                function initialize() {
                    // Initialize default values
                    var mapElem = angular.element(element.children()[3]).children()[0];

                    map = L.map(mapElem, {
                        center: [defLoc.lat, defLoc.lng],
                        zoom: defLoc.accuracy,
                        maxZoom: 21
                    });

                    var roadmap = new L.Google('ROADMAP');
                    var terrain = new L.Google('TERRAIN');
                    var hybrid = new L.Google('HYBRID');
                    map.addLayer(roadmap);

                    var baseLayers = {
                        "Google Streets": roadmap,
                        "Google Terrain": terrain,
                        "Google Hybrid": hybrid
                    };

                    // add layer groups to layer switcher control
                    L.control.layers(baseLayers).addTo(map);

                    // Find input element to use for autocomplete search
                    input = element.find('input');

                    // Create instance for the autocomplete searchbox
                    var autocomplete =
                        new google.maps.places.Autocomplete(input[0]);
                    //autocomplete.setTypes(['geocode']);
                    //autocomplete.bindTo('bounds', map);

                    // Create instance for the reusable marker
                    marker = L.marker([0, 0], {draggable: true});
                    marker.addTo(map);

                    var currentUser = UserService.currentUser();

                    if (currentUser && currentUser.resorts.length > 0 && currentUser.resorts[0].map_kml) {

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

                    // Create instance for the geocoder service
                    geocoder = new google.maps.Geocoder();

                    // Event listener for location change via searchbox
                    google.maps.event.addListener(autocomplete,
                        'place_changed', function () {
                            marker.setOpacity(0);

                            var place = autocomplete.getPlace();
                            if (!place.geometry) {
                                return;
                            }

                            var location = {
                                lat: place.geometry.location.G,
                                lng: place.geometry.location.K
                            };

                            // If the place has a geometry, then present it on a map.
                            map.panTo(location);
                            map.setZoom(zoom);

                            placeMarker(location, false);
                        });

                    // Event listener for map click
                    //L.DomEvent.addListener(map, 'click', function (event) {
                    //    marker.setOpacity(0);
                    //    placeMarker(event.latlng, true);
                    //});

                    L.DomEvent.addListener(marker, 'dragend', function (event) {
                        marker.setOpacity(0);
                        placeMarker(event.target._latlng, true);
                    });

                    // Event listener for map zoom change
                    L.DomEvent.addListener(map,
                        'zoomend',
                        function (event) {
                            zoom = map.getZoom();
                            updateModel();
                        });

                    L.DomEvent.addListener(map,
                        'load',
                        function () {
                            setMap();
                        }, true);

                }

                // Updates the ngModel for the schema form
                function updateModel() {
                    if (ngModel) {
                        var location = marker.getLatLng();

                        if (location) {
                            ngModel.$setViewValue({
                                "lat": location.lat,
                                "long": location.lng,
                                "accuracy": map.getZoom()
                            });
                        }
                    }
                }

                // Place a marker to the map
                function placeMarker(location, updateAddress) {
                    marker.setLatLng(location);
                    marker.setOpacity(1);

                    // Gives a smooth pan to center
                    console.log(location);
                    try{
                    map.panTo(L.latLng(location.lat, location.lng));
} catch(e){}
                    if (updateAddress) {
                        geocoder.geocode({'location': location},
                            function (results, status) {
                                if (status == google.maps.GeocoderStatus.OK) {
                                    if (results[1]) {
                                        input.val(results[1].formatted_address);
                                    } else {
                                        input.val(location.lat +
                                            ', ' + location.lng);
                                    }
                                } else {
                                    console.log('Geocoder failed due to: ' + status);
                                }
                            });
                    }

                    updateModel();
                }

                initialize();

                hotkeys.bindTo(scope).add({
                    combo: 'escape',
                    description: 'Close larger map view',
                    callback: function () {
                        googlemapModalService.dismiss();
                    },
                    persistent: false
                });

                scope.openModal = function () {
                    googlemapModalService
                        .show({
                            lat: marker.getLatLng().lat,
                            lng: marker.getLatLng().lng,
                            accuracy: map.getZoom()
                        })
                        .then(function (result) {
                            map.setZoom(result.accuracy);
                            placeMarker({lat: result.lat, lng: result.lng}, true);
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                };
            }
        }
    }])

    .run(['$templateCache',
        function ($templateCache) {
            var dialogHtml =
                '<div' +
                '   class="image-dialog map-dialog" ng-keypress="onKeyPress($event)">' +
                '   <div class="image-dialog-vertical-center">' +
                '       <a' +
                '           href=""' +
                '           title="Close"' +
                '           class="close-btn"' +
                '           ng-click="onDoneClick($event); $event.preventDefault()">' +
                '           Close' +
                '       </a>' +
                '       <div class="map-dialog-body">' +
                '           <div class="map-larger" style="width:100%;height: 100%;margin: 0px;padding: 0px"></div>' +
                '       </div>' +

                '   </div>' +
                '</div>';
            $templateCache.put('googlemap-dialog.html', dialogHtml);
        }])

    .factory('googlemapModalService',
    ['$rootScope',
        '$animate',
        '$compile',
        '$timeout',
        '$templateCache',
        '$http',
        '$q',
        'UserService',
        function ($rootScope, $animate, $compile, $timeout, $templateCache, $http, $q, UserService) {

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


            var /* Initialize isolated scope */
                scope = $rootScope.$new(true),

                map,
                marker,

            /* Variable to store body element */
                body,

            /* Variable to hold template string to be compiled */
                dialogElem,

                dialogTemplate = 'googlemap-dialog.html',

                onResult,

                buildDialog = function (template) {
                    var dfd = $q.defer();
                    onResult = function (resultData) {
                            if (resultData) {
                                dfd.resolve(resultData);
                            } else {
                                dfd.reject('Modal Canceled');
                            }

                            dismissDialog();
                        };
                        //initZoom = function () {
                            //if (window.Magnifier && window.Event) {
                            //    var evt = new Event(),
                            //        magnifier = new Magnifier(evt);
                            //
                            //    magnifier.attach({
                            //        thumb: '#thumb',
                            //        large: scope.imgSrc,
                            //        mode: 'inside',
                            //        zoom: 3,
                            //        zoomable: true
                            //    });
                            //}
                        //};

                    //scope.imgSrc = scope.options.src;

                    //console.log(scope.options);

                    /* Compiles the template string from $templateCache */
                    dialogElem = $compile(template)(scope);

                    /* Sanity check */
                    if (!body) {
                        body = document.getElementsByTagName('body');
                    }

                    /* Convert body element to angular element */
                    body = angular.element(body);

                    /* Append to body */
                    body.append(dialogElem);

                    //if (scope.options.isZoomable) {
                    //    setTimeout(function () {
                    //        var dialogBody =
                    //            document.getElementsByClassName('image-dialog-body');
                    //
                    //        if (dialogBody && dialogBody.length > 0) {
                    //            var bod = dialogBody[0],
                    //                imgElem = bod.getElementsByTagName('img');
                    //
                    //            if (imgElem && imgElem.length > 0) {
                    //                imgElem = imgElem[0];
                    //                bod.style.width = imgElem.width + 'px';
                    //            }
                    //        }
                    //
                    //        initZoom();
                    //    }, 0);
                    //}

                    setTimeout(function () {
                        var mapElem = document.getElementsByClassName('map-larger');

                        map = L.map(mapElem[0], {
                            center: [scope.options.lat, scope.options.lng],
                            zoom: scope.options.accuracy,
                            keyboard:true,
                            maxZoom: 21
                        });

                        var roadmap = new L.Google('ROADMAP');
                        var terrain = new L.Google('TERRAIN');
                        var hybrid = new L.Google('HYBRID');
                        map.addLayer(roadmap);

                        var baseLayers = {
                            "Google Streets": roadmap,
                            "Google Terrain": terrain,
                            "Google Hybrid": hybrid
                        };

                        // add layer groups to layer switcher control
                        L.control.layers(baseLayers).addTo(map);

                        // Create instance for the reusable marker
                        marker = L.marker([scope.options.lat, scope.options.lng], {draggable: true});
                        marker.addTo(map);

                        var currentUser = UserService.currentUser();

                        if (currentUser && currentUser.resorts.length > 0 && currentUser.resorts[0].map_kml) {

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

                                // Event listener for map click
                                //L.DomEvent.addListener(map, 'click', function (event) {
                                //    marker.setOpacity(0);
                                //    placeMarker(event.latlng);
                                //});

                                L.DomEvent.addListener(marker, 'dragend', function (event) {
                                    marker.setOpacity(0);
                                    placeMarker(event.target._latlng);
                                });

                                // Event listener for map zoom change
                                //L.DomEvent.addListener(map,
                                //    'zoomend',
                                //    function (event) {
                                //        zoom = map.getZoom();
                                //    });

                                map.getContainer().focus();
                            });
                        }

                    }, 0);

                    function placeMarker(location) {
                        marker.setLatLng(location);
                        marker.setOpacity(1);

                        // Gives a smooth pan to center
                        map.panTo(location);
                    }

                    // Dialog done button is click
                    scope.onDoneClick = function ($event) {
                        onResult({
                            lat: marker.getLatLng().lat,
                            lng: marker.getLatLng().lng,
                            accuracy: map.getZoom()
                        });
                        //dismissDialog();
                    };

                    scope.onKeyPress = function ($event) {
                        console.log($event);
                        if ($event.which === 13) {
                            onResult({
                                lat: marker.getLatLng().lat,
                                lng: marker.getLatLng().lng,
                                accuracy: map.getZoom()
                            });
                            //dismissDialog();
                        }
                    };

                    return dfd.promise;
                },

            /* Shows the terms popup */
                showPopup = function (options) {
                    var dfd = $q.defer(),
                        template = $templateCache.get(dialogTemplate);

                    scope.options = options ? options : {};

                    if (template) {
                        buildDialog(template)
                            .then(function (result) {
                                dfd.resolve(result);
                            })
                            .catch(function (error) {
                                dfd.reject(error);
                            });
                    } else {
                        $http.get(dialogTemplate)
                            .success(function (tpl) {
                                $templateCache.put(dialogTemplate, tpl);
                                buildDialog(tpl)
                                    .then(function (result) {
                                        dfd.resolve(result);
                                    })
                                    .catch(function (error) {
                                        dfd.reject(error);
                                    });
                            });
                    }

                    return dfd.promise;
                },

            /* Dismisses the dialog */
                dismissDialog = function () {
                    if (dialogElem) {
                        $animate.leave(dialogElem, function () {
                            dialogElem.remove();
                        });
                    }
                };

            return {
                /* Call this to show dialog */
                show: function (options) {
                    return showPopup(options);
                },

                /* Call this to dismiss dialog */
                dismiss: function () {
                    onResult({
                            lat: marker.getLatLng().lat,
                            lng: marker.getLatLng().lng,
                            accuracy: map.getZoom()
                        });
                }
            }
        }]);