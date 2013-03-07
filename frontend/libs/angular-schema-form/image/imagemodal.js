'use strict';

/**
 * imagemodal Module
 *
 * Description
 */

function generateUUID() {
    var d = new Date().getTime(); //81cbe78a-31b2-448e-a4ed-86c45c580aff
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

angular.module('schemaForm')

    .run(['$templateCache',
        function ($templateCache) {

            $templateCache.put('imagemodal.html',
                    '<div' +
                    '   class="image-modal-wrapper"' +
                    '   ng-class="{' +
                    '       uploading:uploading' +
                    '   }">' +
                    '    <label ng-if="uploading" style="font-size: 24px;text-align: center;width: 100%;">' +
                    '        <i class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></i>' +
                    '        <span>Uploading...</span>' +
                    '    </label>' +
                    '   <img' +
                    '       ng-class="{clickable: !isUploadable || hasImage}"' +
                    '       ng-show="hasImage"' +
                    '       ng-click="onImageClick(); $event.preventDefault()">' +
                    '   <input' +
                    '       ng-if="isUploadable && !hasImage"' +
                    '       accept="image/jpg, image/jpeg, image/png, image/gif, image/bmp"' +
                    '       type="file"' +
                    '       file-reader' +
                    '       on-file-change="onImageChange(files)">' +
                    '   <span class="img-upload-label" ng-show="!hasImage"></span>' +
                    '   <a' +
                    '       class="is-removable"' +
                    '       href=""' +
                    '       ng-if="isRemovable && hasImage"' +
                    '       ng-click="removeImage()">Remove</a>' +
                    '</div>'
            );

            $templateCache.put('imagemodal-dialog.html',
                    '<div' +
                    '   class="image-dialog">' +
                    '   <div class="image-dialog-vertical-center">' +
                    '       <div class="image-dialog-body">' +
                    '           <img' +
                    '               id="thumb"' +
                    '               class="md-card-image"' +
                    '               ng-src="[[imgSrc]]">' +
                    '       </div>' +
                    '       <a' +
                    '           href=""' +
                    '           title="Close"' +
                    '           class="close-btn"' +
                    '           ng-click="onCloseOnMask($event); $event.preventDefault()">' +
                    '           Close' +
                    '       </a>' +
                    '       <div class="button-holder">' +
                    '           <md-button' +
                    '               class="md-raised md-primary"' +
                    '               ng-click="onDoneClick(); $event.preventDefault()">' +
                    '               Close' +
                    '           </md-button>' +
                    '       </div>' +
                    '   </div>' +
                    '</div>'
            );
        }])

// File change listener directive
    .directive('fileReader',
    [function () {
        return {
            // Declared as attribute to activate
            restrict: 'A',

            // Scope values
            scope: {
                onFileChange: '&',
                onFileChangeError: '&'
            },

            link: function (scope, element) {
                element.on('change', function (event) {
                    onFileChange(event.target.files);
                });

                // Use native event ondrop instead of angularjs
                element[0].ondrop = function (event) {
                    event.preventDefault && event.preventDefault();
                    onFileChange(event.dataTransfer.files);
                };

                element[0].ondragenter = function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                };

                element[0].ondragover = function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                };

                function onFileChange(files) {
                    if (files.length > 0) {
                        // Pass callback to parent implementor
                        scope.onFileChange({'files': files});
                        // Clear value on the input field to allow re-upload file
                        element.val(undefined);
                        scope.$apply();
                    }
                }

                element.attr('type', 'file');
            }
        }
    }])

    .directive('imageModal',
    ['imageModalService', 'UploadService', 'IncidentService', '$state', '$log', '$http', '$sce', 'LS', 'growl',
        function (imageModalService, UploadService, IncidentService, $state, $log, $http, $sce, LS, growl) {
            var tz = jstz.determine();

            return {
                // Declared as attribute to initialize
                restrict: 'A',

                require: 'ngModel',

                // Scope values
                scope: {
                    imageSrc: '=ngModel',
                    isUploadable: '=imageIsUploadable',
                    isRemovable: '=imageIsRemovable',
                    isZoomable: '=imageIsZoomable'
                },

                templateUrl: 'imagemodal.html',

                replace: true,

                link: function (scope, element, attr, ngModelCtrl) {
                    var key = Date.now(),

                        formData,

                        img = element.find('img')[0],

                        supportedFileType = [
                            'image/jpeg',
                            'image/png',
                            'image/gif'
                        ];

                    ngModelCtrl.$render = function () {
                        var model = ngModelCtrl.$viewValue;

                        if (model !== undefined && model != null && model.length > 48) { // to only assign value if it is not asset id

                            // Simulate a call to Dropbox or other service that can
                            // return an image as an ArrayBuffer.
                            var xhr = new XMLHttpRequest();

                            // Use JSFiddle logo as a sample image to avoid complicating
                            // this example with cross-domain issues.
                            xhr.open( "GET", model, true );

                            var authorization = LS.get('Authorization');
                            var token = LS.get('token');

                            xhr.setRequestHeader('Authorization', authorization);
                            xhr.setRequestHeader('token', token);

                            // Ask for the result as an ArrayBuffer.
                            xhr.responseType = "arraybuffer";

                            xhr.onload = function( e ) {
                                // Obtain a blob: URL for the image data.
                                var arrayBufferView = new Uint8Array( this.response );
                                var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
                                var urlCreator = window.URL || window.webkitURL;
                                var imageUrl = urlCreator.createObjectURL( blob );
                                img.src = $sce.trustAsResourceUrl(imageUrl);
                            };

                            xhr.send();

                            //scope.assetId = model.id;
                            scope.hasImage = true;
                        }
                    };

                    var previewImage = function (file) {
                        // Check if
                        if (file) {
                            var fileReader = new FileReader();
                            fileReader.readAsDataURL(file);

                            // Called when after readAsDataURL on fileReader
                            fileReader.onloadend = function (res) {
                                img.src = res.target.result;
                            };

                            scope.hasImage = true;

                        } else if (scope.imageSrc) {
                            img.src = scope.imageSrc;
                            scope.hasImage = true;
                        }
                    };

                    var toUTC = function (value) {
                            return moment.tz(value, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
                        };

                    var formatDate = function(value) {
                        return moment(value).format('YYYY-MM-DD');
                    };

                    var dataURItoBlob = function (dataURI) {
                        // convert base64/URLEncoded data component to raw binary data held in a string
                        var byteString;

                        if (dataURI.split(',')[0].indexOf('base64') >= 0) {
                            byteString = dataURI.split(',')[1];
                        } else {
                            byteString = dataURI.split(',')[1];
                        }

                        return byteString;
                    };

                    /* Called when image file has change from fileUploader directive */
                    scope.onImageChange = function (files) {
                        var file = files[0];

                        if (supportedFileType.indexOf(file.type) != -1) {

                            var fileReader = new FileReader(),
                                imgChecker = new Image();

                            fileReader.readAsDataURL(file);

                            // Called when after readAsDataURL on fileReader
                            fileReader.onloadend = function (res) {

                                imgChecker.src = res.target.result;

                                if (scope.isUploadable) {

                                    var incidentId = $state.params.incidentId;

                                    var assetId = generateUUID();

                                    //ngModelCtrl.$modelValue = assetId;
                                    //$log.log(ngModelCtrl);

                                    ngModelCtrl.$setViewValue(assetId);

//                                    $log.log(ngModelCtrl);

                                    var incidentModel = angular.element(jQuery('form')).scope().model;
                                    var incidentdate = angular.element(jQuery('form')).scope().dates;
                                    var incidentdatetime = angular.element(jQuery('form')).scope().datetimes;

                                    var incident_data = {};
                                    $.each(incidentModel, function (k, v) {
                                        if (v instanceof Date) {
                                            if (incidentdatetime.indexOf(k) > -1) {
                                                incident_data[k] = toUTC(v);
                                            }
                                            else if(incidentdate.indexOf(k) > -1) {
                                                incident_data[k] = formatDate(v);
                                            }
                                            else {
                                                incident_data[k] = v;
                                            }
                                        }
                                        else if (v instanceof Array){
                                            var tempArray = [];
                                            v.forEach( function (eachItem){
                                                if (eachItem instanceof Object){
                                                    var tempObject = {};
                                                    $.each(eachItem, function (k1, v1) {
                                                        if (v1 instanceof Date) {
                                                            if (incidentdatetime.indexOf(k1) > -1) {
                                                                tempObject[k1] = toUTC(v1);
                                                            }
                                                            else if (incidentdate.indexOf(k1) > -1) {
                                                                tempObject[k1] = formatDate(v1);
                                                            }
                                                        }
                                                        else {
                                                            tempObject[k1] = v1;
                                                        }
                                                    });
                                                    tempArray.push(tempObject);
                                                }
                                                else{
                                                    tempArray.push(eachItem);
                                                }
                                            });
                                            incident_data[k] = tempArray
                                        }
                                        else {
                                            incident_data[k] = v;
                                        }
                                    });


                                    if (incidentId) {
                                        scope.uploading = true;

                                        IncidentService
                                            .saveIncident(incidentId, incident_data)
                                            .then(function (data) {

                                                var formdata = new FormData();
                                                formdata.append('media', dataURItoBlob(res.target.result));
                                                formdata.append('mimeType', file.type);
//                                                formdata.append('type', 'photo');
                                                formdata.append('media_reference', assetId);

                                                UploadService.upload(incidentId, formdata, file.type).then(function (result) {
                                                    scope.uploading = false;

                                                    $log.log(result.media_url);

                                                    //ngModelCtrl.$modelValue = result.media_url;
                                                    ngModelCtrl.$setViewValue(result.media_url);
                                                    //    {
                                                    //    "imageurl": result.media_url
                                                    //});

                                                    //incidentModel = angular.element(jQuery('form')).scope().model;
                                                    $log.log(ngModelCtrl);

                                                    //incidentModel = JSON.parse(JSON.stringify(incidentModel), function (k, v) {
                                                    //    if (v && v.hasOwnProperty('imageurl')) {
                                                    //        v = v.imageurl;
                                                    //    }
                                                    //
                                                    //    return v;
                                                    //});
                                                    //
                                                    //incidentModel = angular.element(jQuery('form')).scope().model;
                                                    //$log.log(incidentModel);

//                                                    console.log(result);
                                                }).catch(function (error) {
                                                    scope.uploading = false;
                                                    console.log(error);
                                                    growl.error("image_upload_failed");
                                                });

                                            }).catch(function (error) {
                                                scope.uploading = false;
                                                console.log(error);
                                                growl.error("image_upload_failed");
                                            });
                                    }
                                }
                            };

                            // Called when dataUrl loaded on the imgChecker
                            imgChecker.onload = function () {
                                // Show Image modal
                                imageModalService
                                    .show({
                                        "src": imgChecker.src,
                                        "isZoomable": scope.isZoomable
                                    })
                                    .then(function (result) {
                                        img.src = result;
                                        scope.hasImage = true;
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            }
                        } else {
                            // Throw file not supported error
                            alert('File type not supported');
                        }
                    };

                    scope.onImageClick = function () {
                        // Show Image modal
                        imageModalService
                            .show({
                                "src": img.src,
                                "isZoomable": scope.isZoomable
                            })
                            .then(function (result) {
                                // Do nothing
                            })
                            .catch(function (error) {
                                console.log(error);
                            });
                    };

                    scope.removeImage = function () {
                        scope.imageSrc = null;

                        img.src = '';
                        scope.hasImage = false;

//                        localStorage.setItem(attr.id, 'null');
                    };

                    // Initialize
//                    init();
                }
            }
        }])

    .factory('imageModalService',
    ['$rootScope',
        '$animate',
        '$compile',
        '$timeout',
        '$templateCache',
        '$http',
        '$q',
        function ($rootScope, $animate, $compile, $timeout, $templateCache, $http, $q) {
            var /* Initialize isolated scope */
                scope = $rootScope.$new(true),

            /* Variable to store body element */
                body,

            /* Variable to hold template string to be compiled */
                dialogElem,

                dialogTemplate = 'imagemodal-dialog.html',

                buildDialog = function (template) {
                    var dfd = $q.defer(),
                        onResult = function (resultData) {
                            if (resultData) {
                                dfd.resolve(resultData);
                            } else {
                                dfd.reject('ImageModal Canceled');
                            }

                            dismissDialog();
                        },
                        initZoom = function () {
                            if (window.Magnifier && window.Event) {
                                var evt = new Event(),
                                    magnifier = new Magnifier(evt);

                                magnifier.attach({
                                    thumb: '#thumb',
                                    large: scope.imgSrc,
                                    mode: 'inside',
                                    zoom: 3,
                                    zoomable: true
                                });
                            }
                        };

                    scope.imgSrc = scope.options.src;

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

                    if (scope.options.isZoomable) {
                        setTimeout(function () {
                            var dialogBody =
                                document.getElementsByClassName('image-dialog-body');

                            if (dialogBody && dialogBody.length > 0) {
                                var bod = dialogBody[0],
                                    imgElem = bod.getElementsByTagName('img');

                                if (imgElem && imgElem.length > 0) {
                                    imgElem = imgElem[0];
                                    bod.style.width = imgElem.width + 'px';
                                }
                            }

                            initZoom();
                        }, 0);
                    }

                    /* Bind mask click */
                    scope.onCloseOnMask = function ($event) {
                        /* Sanity check */
                        if ($event
                            && $event.target
                            && $event.target.className) {
                            var className = $event.target.className;

                            /* Handle only parent container and close buton */
                            if (className == 'close-btn') {
                                dismissDialog();

                                dfd.reject('ImageModal Canceled');
                            }
                        }
                    };

                    // Dialog done button is click
                    scope.onDoneClick = function () {
                        onResult(scope.options.src);
                        dismissDialog();
                    };

                    return dfd.promise;
                },

            /* Shows the terms popup */
                showPopup = function (options) {
                    var dfd = $q.defer(),
                        template = $templateCache.get(dialogTemplate);

                    scope.options = options ? options : new Object();

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
                    dismissDialog();
                }
            }
        }]);