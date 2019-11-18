/**
 * Directives
 * Author: Shirish Goyal
 */
(function () {
    'use strict';

    angular
        .module('app')
        .directive('backendError', backendError)
        .directive("passwordVerify", passwordVerify)
        .directive("confirmOnExit", confirmOnExit)
        .directive("preventMousewheel", preventMousewheel)
        .directive("ngConfirm", ngConfirm)
        .directive("fileMonitor", fileMonitor)
    ;

    function fileMonitor() {
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

        var fileChanged = function (files, scope, ctrl, element) {
            var file = files[0],
                supportedFileType = [
                    '',
                    'image/gif',
                    'image/jpeg',
                    'image/jpg',
                    'image/png',
                    'application/json',
                    'text/html',
                    'audio/mp3',
                    'video/mp4',
                    'audio/mp4'
                ];

                        //console.log(file);
                        //console.log(file.type);

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
                        var data = (res.target.result);
                        scope.ngModel = data;
                    };
                }

            } else {
                // Throw file not supported error

                alert('File type not supported');
            }
        };

        return {
            // Declared as attribute to activate
            restrict: 'A',

            // Scope values
            scope: {
                ngModel: '=',
                onFileChange: '&'
            },

            link: function (scope, element, attr, ctrl) {
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
                        fileChanged(files, scope, ctrl, element);

                        // Clear value on the input field to allow re-upload file
                        element.val(undefined);
                        scope.$apply();
                    }
                }

                element.attr('type', 'file');
            }
        }
    }

    /**
     * @name backendError
     * @desc Clear backend error if input value has been modified.
     *       This helps in ensuring field is re-validated from backend
     */
    function backendError() {
        return {
            restrict: 'A',
            require: '?ngModel',
            link: function (scope, element, attrs, ctrl) {
                return element.on('change', function () {
                    return scope.$apply(function () {
                        return ctrl.$setValidity('backend', true);
                    });
                });
            }
        };
    }

    function passwordVerify() {
        return {
            require: "ngModel",
            scope: {
                passwordVerify: '='
            },
            link: function (scope, element, attrs, ctrl) {
                scope.$watch(function () {
                    var combined;

                    if (scope.passwordVerify || ctrl.$viewValue) {
                        combined = scope.passwordVerify + '_' + ctrl.$viewValue;
                    }
                    return combined;
                }, function (value) {
                    if (value) {
                        ctrl.$parsers.unshift(function (viewValue) {
                            var origin = scope.passwordVerify;
                            if (origin !== viewValue) {
                                ctrl.$setValidity("passwordVerify", false);
                                return undefined;
                            } else {
                                ctrl.$setValidity("passwordVerify", true);
                                return viewValue;
                            }
                        });
                    }
                });
            }
        };
    }

    function preventMousewheel() {
        return {
            restrict: 'A',
            link: function (scope, $element) {
                $element.on('focus', function () {
                    angular.element(this).on('mousewheel', function (e) {
                        e.preventDefault();
                    });
                });
                $element.on('blur', function () {
                    angular.element(this).off('mousewheel');
                });
            }
        };
    }

    function confirmOnExit() {

        return {
            scope: {
                confirmOnExit: '&',
                confirmMessageWindow: '@',
                confirmMessageRoute: '@',
                confirmMessage: '@'
            },
            link: function ($scope, elem, attrs) {
                window.onbeforeunload = function () {
                    if ($scope.confirmOnExit()) {
                        return $scope.confirmMessageWindow || $scope.confirmMessage;
                    }
                };

                var $locationChangeStartUnbind = $scope.$on('$stateChangeStart', function (event, next, current) {
                    if ($scope.confirmOnExit()) {
                        if (!confirm($scope.confirmMessageRoute || $scope.confirmMessage)) {
                            event.stopImmediatePropagation();
                            event.preventDefault();
                        }
                    }
                });

                $scope.$on('$destroy', function () {
                    window.onbeforeunload = null;
                    $locationChangeStartUnbind();
                });
            }
        };
    }

    function ngConfirm() {
        return {
            priority: 100,
            restrict: 'A',
            link: {
                pre: function (scope, element, attrs) {
                    var msg = attrs.ngConfirm || "Are you sure?";

                    element.bind('click', function (event) {
                        if (!confirm(msg)) {
                            event.stopImmediatePropagation();
                            event.preventDefault();
                        }
                    });
                }
            }
        };
    }

})();