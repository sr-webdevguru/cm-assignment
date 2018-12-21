'use strict';

/**
 File plugin for angular schema form

 Usage:

 angular.module('app', ['schemaForm'])
 .controller('AppCtrl',
 ['$scope',
 function ($scope) {
        $scope.model = {};

        $scope.form = [
            {
                "key": "document1",
                "type": "file",
                "title": "Upload File",

                // Upload button label
                "description": "Upload any file",

                // Upload options
                "upload":  'https://www.googleapis.com/upload/drive/v2/files?uploadType=media' ,

                // Form validation error text
                "errorFileSize": 'File size exceeded.',
                "errorFileType": 'File type is not supported.',
                "errorRequired": 'Please upload a file.'
            }
        ];

        $scope.schema = {
            "type": "object",
            "title": "File Upload",
            "properties": {
                "document1": {}
            },
            "required": []
        };
    }])
 */

function generateUUID() {
    var d = new Date().getTime();
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
            var schemaFileHtml =
                '<div class="form-group" ng-class="{\'has-error\': hasError()}">' +
                '    <div' +
                '        file="form"' +
                '        ng-show="form.key"' +
                '        schema-validate="form"' +
                '        ng-model="$$value$$">' +
                '    </div>' +
                '    <div style="color: #A94442" ng-if="hasError()">' +
                '        <div ng-if="ngModel.$error.fileSize">[[form.errorFileSize]]</div>' +
                '        <div ng-if="ngModel.$error.fileType">[[form.errorFileType]]</div>' +
                '        <div ng-if="ngModel.$error.uploadError">Upload error</div>' +
                '        <div ng-if="ngModel.$error.uploadCanceled">Upload canceled</div>' +
                '    </div>' +
                '</div>';

            var fileHtml =
                '<div>' +
                '    <label' +
                '        style="">' +
                '        [[options.title]]' +
                '    </label>' +
                '    <label class="btn btn-info" ng-if="!file && !uploading">' +
                '        <i ng-if="!uploading" class="glyphicon glyphicon-plus"></i>' +
                '        <input' +
                '            style="display: none"' +
                '            type="file"' +
                '            file-observer' +
                '            on-file-change="onFileChange(files)" />' +
                '        <span ng-if="!uploading">Upload</span>' +
                '    </label>' +
                '    <label class="btn btn-info disabled" ng-if="uploading">' +
                '        <i class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></i>' +
                '        <span>Uploading...</span>' +
                '    </label>' +
                '    <a ng-if="uploading" style="margin-left: 10px" href="" ng-click="stopUpload()">Cancel</a>' +
                '    <div ng-if="file && !uploading">' +
                '        <a class="download_file"' +
                '            target="_blank" download="[[downloadfilename]]"' +
                '            ng-class="{disabled: !file}"' +
                '            ng-click="download()" ' +
//                '            ng-href="[[file]]"' +
                '           >' +
                '            <label><i class="glyphicon glyphicon-download"></i> Download</label>' +
                '        </a>' +
                '        <a style="margin-left: 10px" href="" ng-click="removeFile()">Remove</a>' +
                '    </div>' +
                '</div>';

            $templateCache.put('file/schema-file.html', schemaFileHtml);
            $templateCache.put('file/file.html', fileHtml);

        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var file = function (name, schema, options) {
                if (schema.type === 'file') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'file';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(file);

            //Add to the bootstrap directive
            schemaFormDecoratorsProvider
                .addMapping('bootstrapDecorator',
                'file',
                'file/schema-file.html');
            schemaFormDecoratorsProvider
                .createDirective('file',
                'file/schema-file.html');
        }])
    .directive('fileObserver',
    [function () {
        return {
            // Declared as attribute to activate
            restrict: 'A',

            // Scope values
            scope: {
                onFileChange: '&'
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
                        scope.onFileChange({
                            'files': files
                        });
                        // Clear value on the input field to allow re-upload file
                        element.val(undefined);
                        scope.$apply();
                    }
                }

                element.attr('type', 'file');
            }
        }
    }])

    .directive('file',
    ['$q',
        '$http',
        '$timeout',
        'UploadService', 'IncidentService', '$state', '$sce', 'LS', 'growl',
        function ($q, $http, $timeout, UploadService, IncidentService, $state, $sce, LS, growl) {
            var tz = jstz.determine();

            var ext = function (url) {
                return (url = url.substr(1 + url.lastIndexOf("/")).split('?')[0]).substr(url.lastIndexOf("."))
            };

            return {
                scope: {
                    options: '=file',
                    file: '=ngModel'
                },

                require: 'ngModel',

                restrict: 'A',

                templateUrl: 'file/file.html',

                replace: true,

                link: function (scope, element, attr, ngModel) {

                    ngModel.$render = function () {
                        var model = ngModel.$viewValue;

                        if (model !== undefined && model != null && model.length > 48) { // to only assign value if it is not asset id

                            var extension = ext(model);

                            // Simulate a call to Dropbox or other service that can
                            // return an image as an ArrayBuffer.
                            var xhr = new XMLHttpRequest();

                            // Use JSFiddle logo as a sample image to avoid complicating
                            // this example with cross-domain issues.
                            xhr.open("GET", model, true);

                            var authorization = LS.get('Authorization');
                            var token = LS.get('token');

                            xhr.setRequestHeader('Authorization', authorization);
                            xhr.setRequestHeader('token', token);

                            // Ask for the result as an ArrayBuffer.
                            xhr.responseType = "arraybuffer";

                            xhr.onload = function (e) {
                                // Obtain a blob: URL for the image data.
                                var arrayBufferView = new Uint8Array(this.response);
                                var blob = new Blob([ arrayBufferView ], { type: 'application/'+extension.replace(".", "") });
                                var urlCreator = window.URL || window.webkitURL;
                                var fileURL = urlCreator.createObjectURL(blob);
                                scope.fileURL = $sce.trustAsResourceUrl(fileURL);
                                scope.downloadfilename = "media" + extension;
                            };

                            xhr.send();
                        }
                    };


                    var uploadMap = {},

                        dataURItoBlob = function (dataURI) {
                            // convert base64/URLEncoded data component to raw binary data held in a string
                            var byteString;

                            if (dataURI.split(',')[0].indexOf('base64') >= 0) {
                                byteString = dataURI.split(',')[1];
                            } else {
                                byteString = dataURI.split(',')[1];
                            }

                            return byteString;

                            // separate out the mime component
//                            var mimeString = dataURI
//                                .split(',')[0]
//                                .split(':')[1]
//                                .split(';')[0];


                            // write the bytes of the string to a typed array
//                            var ia = new Uint8Array(byteString.length);
//                            for (var i = 0; i < byteString.length; i++) {
//                                ia[i] = byteString.charCodeAt(i);
//                            }
//
//                            return new Blob([ia], {type: mimeString});
                        },


//            uploadFile = function(url, binary) {
//                var dfd = $q.defer(),
//                    xhr,
//                    options = {
//                        "method": 'POST',
//                        "url": url,
//                        "data": binary
//                    };
//
//                xhr = $http(options);
//
//                xhr.success(function (response) {
//                        dfd.resolve(response);
//                    })
//                    .error(function (error) {
//                        dfd.reject(error);
//                    });
//
//                uploadMap[scope.options.key[0]] = {
//                    "xhr": xhr,
//                    "defer": dfd
//                };
//
//                return dfd.promise;
//            },

                    toUTC = function (value) {
                        return moment.tz(value, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
                    },

                    formatDate = function(value) {
                        return moment(value).format('YYYY-MM-DD');
                    },


                    resetFile = function () {
                            if (ngModel) {
                                ngModel.$setViewValue({});
                                ngModel.$setValidity('fileType', true);
                                ngModel.$setValidity('fileSize', true);
                                ngModel.$setValidity('uploadError', true);
                            }

                            scope.progress = -1;
                        },
                        checkFileValidity = function (file) {
                            var error = undefined,
                                extension = file.name.split('.').pop(),
                                fileTypes = scope.options.fileTypes,
                                fileSizeLimit = scope.options.fileSizeLimit;

                            if (fileTypes !== undefined
                                && fileTypes.length > 0) {
                                var indexOf = fileTypes.indexOf(extension.toLowerCase());

                                if (indexOf == -1) {
                                    if (!error) {
                                        error = {};
                                    }
                                    error.fileType = 'File type is not valid';
                                }
                            }

                            if (fileSizeLimit !== undefined) {
                                fileSizeLimit = 1024 * 1024;

                                if (file.size > fileSizeLimit) {
                                    if (!error) {
                                        error = {};
                                    }
                                    error.fileSize = 'File size is too large';
                                }
                            }

                            return {
                                "error": error
                            }
                        };

                    scope.removeFile = function () {
                        resetFile();
                    };

                    scope.stopUpload = function () {
                        // resetFile();

                        var req = uploadMap[scope.options.key[0]];

                        if (req && req.xhr) {
                            req.defer.reject();
                        }
                    };

                    scope.download = function () {
                        console.log("Downloading...");
//                        if (scope.fileURL != null || scope.fileURL != undefined) {
//                            location.href = scope.fileURL;
//                        }

                        var anchor = angular.element('<a/>');
                        anchor.attr({
                            href: scope.fileURL,
                            target: '_blank',
                            download: scope.downloadfilename
                        })[0].click();
                    };


                    scope.onFileChange = function (files) {
                        var file = files[0],
                            supportedFileType = [
                                'image/gif',
                                'image/jpeg' ,
                                'image/jpg' ,
                                'image/png' ,
//                                'application/pdf',
                                'audio/mp3' ,
//                                'video/mp4',
                                'audio/mp4'
                            ];

//                        console.log(file);

//                        console.log(file.type);
                        if (supportedFileType.indexOf(file.type) != -1) {
                            var fileSizeLimit = 1024 * 1024 * 10; //mb

//                            console.log(file.size);

                            if (file.size > fileSizeLimit) {
                                alert('File size is too large and max size allowed is ' + (fileSizeLimit / (1024 * 1024)) + ' mb');
                            } else {

                                var fileReader = new FileReader(),
                                    imgChecker = new Image();

                                fileReader.readAsDataURL(file);

                                // Called when after readAsDataURL on fileReader
                                fileReader.onloadend = function (res) {
                                    imgChecker.src = res.target.result;


                                    var incidentId = $state.params.incidentId;

                                    var assetId = generateUUID();

                                    ngModel.$setViewValue(assetId);

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
//                                            formdata.append('type', 'photo');
                                                formdata.append('media_reference', assetId);

                                                UploadService.upload(incidentId, formdata, file.type).then(function (result) {
                                                    scope.uploading = false;
                                                    scope.file = result.media_url;
//                                                    ngModel.$setViewValue(result.media_url);

                                                }).catch(function (error) {
                                                    scope.uploading = false;
                                                    growl.error("file_upload_failed");
                                                });

                                            })
                                            .catch(function (error) {
                                                scope.uploading = false;
                                                growl.error("file_upload_failed");
                                            });
                                    }

                                };
                            }

                        } else {
                            // Throw file not supported error

                            alert('File type not supported');
                        }


//                        var url = scope.options.upload,
//                            formData = new FormData(),
//                            extension = file.name.split('.').pop(),
//                            fileValidity = checkFileValidity(file),
//                            fileError = fileValidity.error;
//
//                        resetFile();
//
//                        if (fileError) {
//                            // Fire error to schemaForm
//                            if (ngModel) {
//                                if (fileError.fileType == 'error') {
//                                    ngModel.$setValidity('fileType', false);
//                                }
//
//                                if (fileError.fileSize == 'error') {
//                                    ngModel.$setValidity('fileSize', false);
//                                }
//                            }
//
//                            scope.$emit("schemaFormValidate");
//                        }
//                        else {
//                            var fileReader = new FileReader();
//
//                            fileReader.readAsDataURL(file);
//
//                            // Called when after readAsDataURL on fileReader
//                            fileReader.onloadend = function (res) {
//                                var binary = res.target.result,
//                                    url = scope.options.upload;
//
//                                if (url) {
//
//                                    scope.uploading = true;
//
//                                    scope.$apply();
//
//                                    uploadFile(url, binary)
//                                        .then(function (result) {
//                                            scope.uploading = false;
//
//                                            // TODO: Decide what server
//                                            // response model should we follow
//                                            scope.file = {
//                                                "url": '',
//                                                "name": file.name
//                                            };
//                                        })
//                                        .catch(function (error) {
//                                            scope.uploading = false;
//
//                                            if (ngModel) {
//                                                if (error) {
//                                                    ngModel
//                                                        .$setValidity('uploadError',
//                                                        false);
//                                                } else {
//                                                    ngModel
//                                                        .$setValidity('uploadCanceled',
//                                                        false);
//                                                }
//
//                                                scope.$emit("schemaFormValidate");
//                                            }
//                                        })
//                                        .finally(function () {
//                                            uploadMap = new Object();
//                                        });
//                                }
//                            };
//                        }
                    };
                }
            };
        }]);
