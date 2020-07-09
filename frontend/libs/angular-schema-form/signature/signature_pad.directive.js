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
            $templateCache
                .put('directives/decorators/bootstrap/signature.html',
                    '<div class="form-group m-signature">' +
                    '   <label class="control-label" ng-show="showTitle()">[[form.title]]</label>' +

                    '    <div' +
                    //'        name="[[form.key]]"' +
                    '        ng-show="form.key"' +
                    '        class="form-control m-signature-pad"' +
                    '        schema-validate="form" signature' +
                    '        ng-model="$$value$$"' +
                    '    >' +

                    '       <div class="m-signature-pad--body">' +
                         '    <label ng-if="uploading" style="font-size: 16px;text-align: center;width: 100%;">' +
                    '        <i class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></i>' +
                    '        <span>Uploading...</span>' +
                    '    </label>' +
                    '           <img width="676" height="208" ng-show="hasSignature" ng-src="[[imgSrc]]">' +
                    '           <canvas width="676" height="208" ng-hide="hasSignature"></canvas>' +
                    '       </div>' +
                    '       <div class="m-signature-pad--footer">' +
                    '           <div class="description"><a class="btn button clear" data-action="clear">Clear</a> <span ng-hide="hasSignature">Sign above</span><a class="btn button save" ng-hide="hasSignature" data-action="save">Save</a></div>' +
                    '               ' +
                    '               ' +
                    '       </div>' +
                    '   </div>' +
                    '</div>');
        }])
    .config(['schemaFormProvider',
        'schemaFormDecoratorsProvider',
        'sfPathProvider',
        function (schemaFormProvider, schemaFormDecoratorsProvider, sfPathProvider) {

            var imagemodal = function (name, schema, options) {
                if (schema.type === 'signature' && schema.format === 'string') {
                    var f = schemaFormProvider.stdFormObj(name, schema, options);
                    f.key = options.path;
                    f.type = 'signature';
                    options.lookup[sfPathProvider.stringify(options.path)] = f;
                    return f;
                }
            };

            schemaFormProvider.defaults.string.unshift(imagemodal);

            //Add to the bootstrap directive
            schemaFormDecoratorsProvider
                .addMapping('bootstrapDecorator',
                'signature',
                'directives/decorators/bootstrap/signature.html');
            schemaFormDecoratorsProvider
                .createDirective('signature',
                'directives/decorators/bootstrap/signature.html');
        }])
    .directive('signature', ['LS', 'UploadService', 'IncidentService', '$state', '$log', 'growl', function (LS, UploadService, IncidentService, $state, $log, growl) {
        var tz = jstz.determine();

        return {
            restrict: 'A',
            require: '?ngModel',
            link: function (scope, element, attrs, ngModel) {
                if (!ngModel) return;

                var canvas = element.find("canvas")[0];
                var ctx = canvas.getContext("2d");
                var clearButton = element.find("[data-action=clear]"),
                    saveButton = element.find("[data-action=save]");

                var signaturePad = new SignaturePad(canvas);

                ngModel.$render = function () {
                    var model = ngModel.$viewValue;

                    if (model !== undefined && model != null && model.length > 48 && model.indexOf('base64') < 0) { // to only assign value if it is not asset id

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
                            var uInt8Array = new Uint8Array(this.response);
                            var i = uInt8Array.length;
                            var binaryString = new Array(i);
                            while (i--) {
                                binaryString[i] = String.fromCharCode(uInt8Array[i]);
                            }
                            var data = binaryString.join('');

                            // Base64 encoded image and assign it to the scope
                            scope.imgSrc = 'data:image/png;base64,' + window.btoa(data);
                            scope.hasSignature = true;
                        };

                        xhr.send();
                    }
                };

//                signaturePad.onEnd = function () {
//                    scope.$evalAsync(read);
//                };
//                read();
//
//                function read() {
//                    var dataUrl = signaturePad.toDataURL();
//                    ngModel.$setViewValue(dataUrl);
//                }

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

                clearButton.on("click", function (event) {
                    scope.hasSignature = false;
                    signaturePad.clear();
                });

                saveButton.on("click", function (event) {
                    if (signaturePad.isEmpty()) {
                        alert("Please provide signature first.");
                    } else {

                        scope.uploading = true;

                        var incidentId = $state.params.incidentId;
                        var incidentModel = angular.element(jQuery('form')).scope().model;
                        var incidentdate = angular.element(jQuery('form')).scope().dates;
                        var incidentdatetime = angular.element(jQuery('form')).scope().datetimes;
                        var assetId = generateUUID();

                        var image = signaturePad.toDataURL();

                        ngModel.$setViewValue(assetId);

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

                        IncidentService
                            .saveIncident(incidentId, incident_data)
                            .then(function (data) {

                                var formdata = new FormData();
                                formdata.append('media', dataURItoBlob(image));
                                formdata.append('mimeType', 'image/png');
                                formdata.append('media_reference', assetId);

                                UploadService.upload(incidentId, formdata, 'image/png').then(function (result) {
                                    scope.uploading = false;
                                    ngModel.$setViewValue(result.media_url);

                                    scope.hasSignature = true;
                                    scope.imgSrc = image;

                                }).catch(function (error) {
                                    scope.uploading = false;
                                    $log.log(error);
                                    growl.error("signature_upload_failed");
                                });

                            }).catch(function (error) {
                                scope.uploading = false;
                                $log.log(error);
                                growl.error("signature_upload_failed");
                            });
                    }
                });
            }
        }
    }])
;