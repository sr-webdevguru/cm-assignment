'use strict';

angular.module('app')
    .controller('ConfirmModalCtrl', ['$scope', '$modalInstance', function ($scope, $modalInstance) {

        $scope.ok = function () {
            $modalInstance.close(true);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }])
    .controller('IncidentUpdateCtrl',
    ['$scope',
        '$location', '$state', '$rootScope', '$timeout', '$stateParams', '$log', '$filter', 'IncidentService',
        'questions', 'growl', 'UploadService', '$http', '$translate', '$intercom', 'currentUser', '$sce',
        'ApiService', 'CONFIG', 'LS', '$uimodal',
        function ($scope, $location, $state, $rootScope, $timeout, $stateParams, $log, $filter, IncidentService, questions, growl, UploadService, $http, $translate, $intercom, currentUser, $sce, ApiService, CONFIG, LS, $modal) {

            jQuery(':input[type=number]').on('mousewheel', function (e) {
                e.preventDefault();
            });


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

            var id = $stateParams.incidentId;
            var tz = jstz.determine();

            var datetimeFormat = currentUser.resorts[0].datetime_format.key;
            $scope.datetimeFormat = datetimeFormat;
            LS.set('datetimeFormat', datetimeFormat);
            var dateFormat = datetimeFormat.slice(0,10);

            $scope.model = {'dateTimeFormat': datetimeFormat};
            $scope.userRole = currentUser.role;
            $scope.userConnected = currentUser.user_connected.key;

            function setDirty() {
                //$scope.clean = false;
            }

            function setClean() {
                //$scope.clean = true;
                $scope.orig = angular.copy($scope.model);
            }

            function isDirty() {
                var origCopy = angular.copy($scope.orig);
                var newCopy = angular.copy($scope.model);
                removeNulls(origCopy);
                removeNulls(newCopy);

                var difference = diff.getDiff(origCopy, newCopy);

                return !_.isEmpty(difference);

                //return !angular.equals(origCopy, newCopy);
            }

            //var questions = QuestionService.fetch();

            // Pass this function to be used for imagemodal and
            // file plugin to perform upload function.
            var uploadFn = function (formData, type) {
                return UploadService.upload(id, formData, type);
            };

            function toUTC(value) {
                return moment.tz(value, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
            }

            function formatDate(value) {
                return moment(value).format('YYYY-MM-DD');
            }

            function toLocalTime(value) {
                return moment.utc(value, 'YYYY-MM-DD HH:mm:ss').tz(tz.name()).toDate();
            }

            function toLocalDate(value) {
                return moment(value, 'YYYY-MM-DD').toDate();
            }

            $scope.print = function () {
                $log.log('printing incident ' + id);
                growl.info('PRINTING');

                if (id !== null || id !== undefined) {
                    var xhr = new XMLHttpRequest();

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
                        var blob = new Blob([arrayBufferView], {type: 'application/pdf'});
                        var urlCreator = window.URL || window.webkitURL;
                        var fileURL = urlCreator.createObjectURL(blob);
                        fileURL = $sce.trustAsResourceUrl(fileURL);
                        var downloadfilename = id + ".pdf";

                        var anchor = angular.element('<a/>');
                        anchor.attr({
                            href: fileURL,
                            target: '_blank',
                            download: downloadfilename
                        })[0].click();
                    };

                    xhr.send();
                }
            };

            $scope.schema = {
                type: "object",
                properties: {}
            };

            //$scope.model = {
            //    photos: []
            //};

            // Schema Form type
            // "type": "string"	text
            // "type": "number"	number
            // "type": "integer"	number
            // "type": "boolean"	checkbox
            // "type": "object"	fieldset
            // "type": "string" and a "enum"	select
            // "type": "array" and a "enum" in array type	checkboxes
            // "type": "array"	array

            var schema_type = {
                'email': 'string',
                'text': 'string',
                'textarea': 'string',
                'number': 'number',
                'decimal': 'number',
                'range': 'number',
                'patient_age': 'number',
                'arrows': 'string',
                'select': 'string',
                'multi_select': 'object',
                'radio': 'string',
                'gender': 'string',
                'image': 'string',
                'date_picker': 'object',
                'date_time_picker': 'object',
                'google_map': 'object',
                'file': 'string',
                'hidden': 'hidden',
                'timer': 'hidden',
                'message': 'string',
                'signature': 'string',
                'repeater': 'object',
                'distance': 'number',
                'temperature': 'number',
                'weight': 'number',
                'altitude': 'number',
                'length': 'number',
                'height': 'number',
                'radio_button': 'string'
            };

            // Form Type	Becomes
            // fieldset	a fieldset with legend
            // section	just a div
            // conditional	a section with a ng-if
            // actions	horizontal button list, can only submit and buttons as items
            // text	input with type text
            // textarea	a textarea
            // number	input type number
            // password	input type password
            // checkbox	a checkbox
            // checkboxes	list of checkboxes
            // select	a select (single value)
            // submit	a submit button
            // button	a button
            // radios	radio buttons
            // radios-inline	radio buttons in one line
            // radiobuttons	radio buttons with bootstrap buttons
            // help	insert arbitrary html
            // tab	tabs with content
            // array	a list you can add, remove and reorder
            // tabarray	a tabbed version of array

            var form_type = {
                'email': 'email',
                //'email': 'string',
                'text': 'text',
                'range': 'number',
                'patient_age': 'number',
                'textarea': 'textarea',
                'number': 'number',
                'decimal': 'decimal',
                'arrows': 'select',
                'select': 'select',
                'multi_select': 'multiselect',
                'radio': 'radios-inline',
                'gender': 'radios-inline',
                'radio_button': 'radiobuttons',
                'image': 'image',
                //'message': 'help',
                'date_picker': 'datepicker',
                //'date_picker': 'string',
                'date_time_picker': 'datepicker',
                'google_map': 'googlemap',
                'file': 'file',
                'hidden': 'hidden',
                'timer': 'hidden',
                'message': 'message',
                'signature': 'signature',
                'repeater': 'repeater',
                'distance': 'distance',
                'temperature': 'temperature',
                'weight': 'weight',
                'altitude': 'altitude',
                'length': 'length',
                'height': 'heightsf'
            };

            var getChoiceMap = function (mapValues) {
                var _choices = [],
                    _titlemap = [];

                // Loop and build choices and titlemap
                angular.forEach(mapValues, function (value) {
                    for (var key in value) {
                        //console.log(value[key]);
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

            var integers = [];
            var floats = [];
            var selects = [];
            var repeaters = [];

            var datetimes = [];
            var dates = [];

            var errorMap = {};

            var validateNumber = function (modelValue, form, isInteger) {
//                console.log("form is", form);
//                console.log("model is", modelValue);
//                console.log("isInteger ", isInteger);

//                var integer = /^(\-)?\d+$/;
//                var decimal = /^(\-)?\d+(\.\d)?$/;
//
//                if (!isInteger) {
//                    if (modelValue == undefined || !decimal.test(modelValue)) {
//                        var description = 'Invalid decimal value. Decimal value with only 1 decimal point allowed.';
//
//                        $scope.$broadcast('schemaForm.error.'+form.key,'not_valid_decimal', false);
//
//                        growl.error(description);
//                    }
//                } else {
//                    if (modelValue == undefined || !integer.test(modelValue)) {
//                        var description = 'Only integer values allowed';
//
//
////                        $scope.$broadcast('schemaFormValidate');
//                        $scope.$broadcast('schemaForm.error.'+form.key,0, false);
//                        growl.error(description);
//                    }
//                }
            };

            //var identify_variant = function (item, append) {
            //    //if (append == undefined || append == null || append == "") {
            //    //
            //    //} else {
            //    //
            //    //}
            //
            //};

            $scope.has_dob = false;
            $scope.has_age = false;
            var defaults = {};

            var process_tabs = function (tabs) {
                var tab_items = [];

                for (var key in tabs) {
                    if (tabs.hasOwnProperty(key)) {

                        var question_items = [];
                        var repeating_question_items = [];

                        var form_items = [];

                        for (var question in tabs[key]) {
                            // Check if if single schema object
                            if (tabs[key].hasOwnProperty(question)
                                && (question == 'Questions')) {

                                for (var m in tabs[key][question]) {
                                    if (tabs[key][question].hasOwnProperty(m)) {

                                        var q = tabs[key][question][m];

                                        if (q.hasOwnProperty("Default")) {
                                            defaults[m] = tabs[key][question][m]["Default"];
                                        }

                                        var choices = [];
                                        var titlemap = [];

                                        if (m == 'dob') {
                                            $scope.has_dob = true;
                                        }

                                        if (q.Type == 'patient_age') {
                                            $scope.has_age = true;
                                        }

                                        if (q.Type == 'select'
                                            || q.Type == 'arrows'
                                            || q.Type == 'multi_select') {

                                            var choiceMap = getChoiceMap(q.Values);

                                            choices = choiceMap.choices;
                                            titlemap = choiceMap.titlemap;
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

                                        if(q.Type == 'radio_button'){
                                            for (var i = 0; i < q.Values.length; i++) {
                                                titlemap.push({
                                                    value: Object.keys(q.Values[i])[0],
                                                    name: q.Values[i][Object.keys(q.Values[i])[0]]
                                                });
                                            }
                                        }

                                        var item = {
                                            'field': m,
                                            'label': $translate.instant(q.Label),
                                            'type': form_type[q.Type],
                                            'required': q.Required,
                                            'placeholder': $translate.instant(q.Placeholder),
                                            'choices': choices,
                                            'order': q.Order,
                                            'fieldAddonRight': q.Append
                                        };

                                        errorMap[m] = $translate.instant(q.Label);

//                                        identify_variant(item, q.Append);

                                        // If type == image, enable image plugin
//                                        if (q.Type == 'image') {
//                                            item['format'] = 'image';
//                                            item['enableUpload'] = true;
//                                            item['enableRemove'] = true;
//                                            item['enableZoom'] = true;
//                                        }


//                                        if (q.Type != 'message') {

                                        var qForm = {
                                            'field': m,
                                            "key": m,
                                            "type": form_type[q.Type],
                                            "placeholder": $translate.instant(q.Placeholder),
                                            "order": q.Order,
                                            "fieldAddonRight": q.Append,
                                            "tab": $translate.instant(tabs[key].Label)
                                        };

                                        //identify_variant(qForm, q.Append);

                                        if (q.hasOwnProperty('ShowIf')) {
                                            var condition = '';
                                            jQuery.each(q.ShowIf, function (key, value) {
                                                condition += key + "=='" + value + "'";
                                            });
                                            qForm['condition'] = 'model.' + condition;
                                        }

                                        qForm['unit'] = currentUser.resorts[0].unit_format.value;

                                        if (q.Type == 'number' || q.Type == 'range' || q.Type == 'decimal' || q.Type == 'patient_age') {


                                            if (q.hasOwnProperty('Min')) {
                                                qForm['min'] = q.Min;
                                            }

                                            if (q.hasOwnProperty('Max')) {
                                                qForm['max'] = q.Max;
                                            }


                                            var range_message = '';
                                            if (q.hasOwnProperty('Min') && q.hasOwnProperty('Max')) {
                                                range_message = 'in range ' + qForm['min'] + ' - ' + qForm['max'] + ' ';
                                            }


                                            if (q.Type == 'decimal') {
//                                                if (q.hasOwnProperty('Increment')) {
                                                qForm['step'] = 0.1;
                                                qForm['pattern'] = /(\-)?[0-9]+(\.[0-9])?/;
                                                qForm['description'] = 'Decimal value ' + range_message + 'with only 1 decimal point allowed.';
                                                qForm['onChange'] = function (modelValue, form) {
                                                    validateNumber(modelValue, form, false);
                                                    //setDirty();
                                                };
//                                                }
                                            } else {
//                                                if (q.hasOwnProperty('Increment')) {
                                                qForm['step'] = 1;
                                                qForm['pattern'] = /(\-)?[0-9]+/;
                                                qForm['description'] = 'Only integer values ' + range_message + 'allowed.';
                                                qForm['validationMessage'] = {
                                                    0: "Not a valid integer",
                                                    105: "Not a valid integer"
                                                };
                                                qForm['onChange'] = function (modelValue, form) {
                                                    validateNumber(modelValue, form, false);
                                                    //setDirty();
                                                };
//                                                }
                                            }
                                        } else {
                                            qForm['onChange'] = function (modelValue, form) {
                                                //setDirty();
                                            };
                                        }

                                        if (q.Type == 'number' || q.Type == 'range' || q.Type == 'patient_age') {
                                            integers.push(m);
                                        }

                                        if (q.Type == 'decimal') {
                                            floats.push(m);
                                        }
                                        //
                                        //if (q.Type == 'select' || q.Type == 'arrows') {
                                        //    selects.push(m);
                                        //}

                                        if (q.Type == 'multi_select') {
                                            qForm["choices"] = choices;
                                        } else {
                                            qForm["titleMap"] = titlemap;
                                        }

                                        if (q.Type == 'date_picker') {
                                            qForm["dateFormat"] = dateFormat;
                                            qForm["placeholder"] = dateFormat;
                                            qForm["description"] = "Date should be of the format " + dateFormat + " and/or invalid date";
                                            qForm["picker_type"] = "date";
                                            dates.push(m);
                                        }

                                        if (q.Type == 'date_time_picker') {
                                            qForm["dateFormat"] = datetimeFormat;
                                            qForm["placeholder"] = datetimeFormat;
                                            qForm["description"] = "Datetime should be of the format " + datetimeFormat + " and/or invalid datetime";
                                            qForm["picker_type"] = "datetime";
                                            datetimes.push(m);
                                        }

                                        $scope.schema.properties[m] = {
                                            'title': $translate.instant(q.Label),
                                            'type': schema_type[q.Type],
                                            'order': q.Order,
                                        };

                                        // If type == image, assign format image
                                        // to use imagemodal plugin
                                        if (q.Type == 'image' || q.Type == 'signature') {
//                                                qForm['format'] = 'image';
                                            qForm['enableUpload'] = true;
                                            qForm['enableRemove'] = true;
                                            qForm['enableZoom'] = true;
                                        }

                                        // Handles the repeater type forms
                                        if (q.Type == 'repeater'
                                            && q.hasOwnProperty('RepeatingQuestions')) {

                                            repeaters.push(m);

                                            var repeaterForm = [];
                                            var repeaterSchema = {
                                                type: 'object',
                                                properties: {},
                                                required: []
                                            };

                                            // Loop through the repeating question
                                            // for the repeater model property
                                            var tabkey = key;
                                            angular.forEach(q.RepeatingQuestions,
                                                function (value, key) {
                                                    var repForm = {
                                                        'field': key,
                                                        "key": key,
                                                        "title": $translate.instant(value.Label),
                                                        "type": form_type[value.Type],
                                                        "placeholder": $translate.instant(value.Placeholder),
                                                        "order": value.Order,
                                                        "fieldAddonRight": value.Append,
                                                        "ngModelOptions": {
                                                            "updateOn": 'blur'
                                                        },
                                                        "tab": $translate.instant(tabs[tabkey].Label)
                                                    };

                                                    errorMap[key] = $translate.instant(value.Label);

                                                    //identify_variant(repForm, value.Append);

                                                    if (value.hasOwnProperty('ShowIf')) {
                                                        var condition = '';
                                                        jQuery.each(value.ShowIf, function (k, v) {
                                                            condition += k + "=='" + v + "'";
                                                        });
                                                        repForm['condition'] = 'model.' + condition;
                                                    }

                                                    //if (q.Type == 'number') {
                                                    //    floats.push(key);
                                                    //}
                                                    //
                                                    //if (q.Type == 'select' || q.Type == 'arrows') {
                                                    //    selects.push(key);
                                                    //}

                                                    if (value.Type == 'patient_age') {
                                                        $scope.has_age = true;
                                                    }

                                                    // Setup form to handle other field types
                                                    if (value.Type == 'select'
                                                        || value.Type == 'arrows'
                                                        || value.Type == 'multi_select') {
                                                        var repChoiceMap =
                                                            getChoiceMap(value.Values);

                                                        repForm.choices
                                                            = repChoiceMap.choices;
                                                        repForm.titleMap
                                                            = repChoiceMap.titlemap;
                                                    }

                                                    if (value.Type == 'date_picker') {
                                                        repForm["dateFormat"] =
                                                            dateFormat;
                                                        repForm["placeholder"] = dateFormat;
                                                        qForm["description"] = "Date should be of the format " + dateFormat + " and/or invalid date";
                                                        qForm["picker_type"] = "date";
                                                        dates.push(key);
                                                    }

                                                    if (value.Type == 'date_time_picker') {
                                                        repForm["dateFormat"] =
                                                            datetimeFormat;
                                                        repForm["placeholder"] = datetimeFormat;
                                                        qForm["description"] = "Datetime should be of the format " + datetimeFormat + " and/or invalid datetime";
                                                        qForm["picker_type"] = "datetime";
                                                        datetimes.push(key);
                                                    }

                                                    repForm['unit'] = currentUser.resorts[0].unit_format.value;

                                                    if (value.Type == 'number' || value.Type == 'range' || value.Type == 'decimal' || value.Type == 'patient_age') {
                                                        if (value.hasOwnProperty('Min')) {
                                                            repForm['min'] = value.Min;
                                                        }

                                                        if (value.hasOwnProperty('Max')) {
                                                            repForm['max'] = value.Max;
                                                        }

                                                        var range_message = '';
                                                        if (value.hasOwnProperty('Min') && value.hasOwnProperty('Max')) {
                                                            range_message = 'in range ' + repForm['min'] + ' - ' + repForm['max'] + ' ';
                                                        }


                                                        if (value.Type == 'decimal') {
                                                            //                                                if (q.hasOwnProperty('Increment')) {
                                                            repForm['step'] = 0.1;
                                                            repForm['pattern'] = /(\-)?[0-9]+(\.[0-9])?/;
                                                            repForm.description = 'Decimal value ' + range_message + 'with only 1 decimal point allowed.';
                                                            repForm['onChange'] = function (modelValue, form) {
                                                                validateNumber(modelValue, form, false);
                                                                //setDirty();
                                                            };

                                                            //                                                }
                                                        } else {
                                                            //                                                if (q.hasOwnProperty('Increment')) {
                                                            repForm['step'] = 1;
                                                            repForm['pattern'] = /(\-)?[0-9]+/;
                                                            qForm.description = 'Only integer values ' + range_message + 'allowed.';
                                                            repForm['validationMessage'] = {
                                                                0: "Not a valid integer",
                                                                105: "Not a valid integer"
                                                            };
                                                            repForm['onChange'] = function (modelValue, form) {
                                                                validateNumber(modelValue, form, true);
                                                                //setDirty();
                                                            };
                                                            //                                                }
                                                        }

                                                    } else {
                                                        repForm['onChange'] = function (modelValue, form) {
                                                            //setDirty();
                                                        };
                                                    }

                                                    if (value.Type == 'number' || value.Type == 'range' || value.Type == 'patient_age') {
                                                        integers.push(key);
                                                    }

                                                    if (q.Type == 'decimal') {
                                                        floats.push(key);
                                                    }

                                                    // Initialize repeater schema
                                                    // properties
                                                    repeaterSchema.properties[key] = {
                                                        "type": schema_type[value.Type]
                                                    };

                                                    // Add to repeater schema if such
                                                    // model property is required
                                                    if (value.Required == 'true') {
                                                        repeaterSchema
                                                            .required.push(key);
                                                    }

                                                    // Store repeater form config
                                                    repeaterForm.push(repForm);
                                                });

                                            // Assign to repeater form
                                            qForm.form = repeaterForm;
                                            qForm.schema = repeaterSchema;

                                            //console.log(qForm.schema);
                                        }

                                        form_items.push(qForm);
//                                        }

                                        // $log.info(item);

                                        question_items.push(item);
                                    }
                                }
                            }

                            // Check if array of schema objects
                            if (tabs[key].hasOwnProperty(question)
                                && (question == 'RepeatingQuestions')) {

                                repeaters.push(key);

                                $scope.schema.properties[key] = {
                                    type: "array",
                                    items: {
                                        type: "object",
                                        properties: {}
                                    }
                                };

                                var l = {
                                    key: key,
                                    title: '',
                                    add: "Add",
                                    style: {
                                        add: "btn-success"
                                    },
                                    items: []
                                };

//                                if ($scope.userRole == 'Patroller') {
//                                    l['readonly'] = true;
//                                }

                                for (var m in tabs[key][question]) {
                                    if (tabs[key][question].hasOwnProperty(m)) {

                                        // $log.log("key: " + m);

                                        var q = tabs[key][question][m];

//                                console.log(q.Type);

                                        if (m == 'dob') {
                                            $scope.has_dob = true;
                                        }

                                        if (m.indexOf("&") > -1) {
                                            // $log.log("has & inside");
                                            m = m.replace(' ', '_');
                                            m = m.replace(' ', '_');
                                            m = m.replace('&', '');
                                        }

                                        var choices = [];
                                        var titlemap = [];

                                        //if (q.Type == 'number') {
                                        //    floats.push(m);
                                        //}
                                        //
                                        //if (q.Type == 'select' || q.Type == 'arrows') {
                                        //    selects.push(m);
                                        //}

                                        if (q.Type == 'patient_age') {
                                            $scope.has_age = true;
                                        }

                                        if (q.Type == 'select'
                                            || q.Type == 'arrows'
                                            || q.Type == 'multi_select') {

                                            var choiceMap = getChoiceMap(q.Values);

                                            choices = choiceMap.choices;
                                            titlemap = choiceMap.titlemap;
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

                                        if(q.Type == 'radio_button'){
                                            for (var i = 0; i < q.Values.length; i++) {
                                                titlemap.push({
                                                    value: Object.keys(q.Values[i])[0],
                                                    name: q.Values[i][Object.keys(q.Values[i])[0]]
                                                });
                                            }
                                        }

//                                        if (q.Type != 'message') {
                                        $scope.schema.properties[key].items.properties[m] = {
                                            'title': $translate.instant(q.Label),
                                            'type': schema_type[q.Type],
                                            'order': q.Order
                                        };

                                        var qForm = {
                                            'field': key + '[].' + m,
                                            "key": key + '[].' + m,
                                            "type": form_type[q.Type],
                                            "placeholder": $translate.instant(q.Placeholder),
                                            "order": q.Order,
                                            "tab": $translate.instant(tabs[key].Label)
                                        };


                                        if (q.hasOwnProperty('ShowIf')) {
                                            var condition = '';
                                            jQuery.each(q.ShowIf, function (key, value) {
                                                condition += key + "=='" + value + "'";
                                            });
                                            qForm['condition'] = 'model.' + condition;
                                        }

                                        if (q.Type == 'multi_select') {
                                            qForm["choices"] = choices;
                                        } else {
                                            qForm["titleMap"] = titlemap;
                                        }

                                        if (q.Type == 'date_picker') {
                                            qForm["dateFormat"] = dateFormat;
                                            qForm["placeholder"] = dateFormat;
                                            qForm["description"] = "Date should be of the format " + dateFormat + " and/or invalid date";
                                            qForm["picker_type"] = "date";
                                            dates.push(m);
                                        }

                                        if (q.Type == 'date_time_picker') {
                                            qForm["dateFormat"] = datetimeFormat;
                                            qForm["placeholder"] = datetimeFormat;
                                            qForm["description"] = "Datetime should be of the format " + datetimeFormat + " and/or invalid datetime";
                                            qForm["picker_type"] = "datetime";
                                            datetimes.push(m);
                                        }

                                        // modify qForm for imagemodal plugin
                                        if (q.Type == 'image' || q.Type == 'signature') {
//                                                qForm['format'] = 'image';
                                            qForm['enableUpload'] = true;
                                            qForm['enableRemove'] = true;
                                            qForm['enableZoom'] = true;
                                        }

                                        qForm['unit'] = currentUser.resorts[0].unit_format.value;

                                        if (q.Type == 'number' || q.Type == 'range' || q.Type == 'decimal' || q.Type == 'patient_age') {

                                            if (q.hasOwnProperty('Min')) {
                                                qForm['min'] = q.Min;
                                            }

                                            if (q.hasOwnProperty('Max')) {
                                                qForm['max'] = q.Max;
                                            }

                                            var range_message = '';
                                            if (q.hasOwnProperty('Min') && q.hasOwnProperty('Max')) {
                                                range_message = 'in range ' + qForm['min'] + ' - ' + qForm['max'] + ' ';
                                            }


                                            if (q.Type == 'decimal') {
//                                                if (q.hasOwnProperty('Increment')) {
                                                qForm['step'] = 0.1;
                                                qForm['pattern'] = /(\-)?[0-9]+(\.[0-9])?/;
                                                qForm['description'] = 'Decimal value ' + range_message + 'with only 1 decimal point allowed.';
                                                qForm['onChange'] = function (modelValue, form) {
                                                    validateNumber(modelValue, form, false);
                                                    //setDirty();
                                                };
//                                                }
                                            } else {
//                                                if (q.hasOwnProperty('Increment')) {
                                                qForm['step'] = 1;
                                                qForm['pattern'] = /(\-)?[0-9]+/;
                                                qForm['description'] = 'Only integer values ' + range_message + 'allowed.';
                                                qForm['validationMessage'] = {
                                                    0: "Not a valid integer",
                                                    105: "Not a valid integer"
                                                };
                                                qForm['onChange'] = function (modelValue, form) {
                                                    validateNumber(modelValue, form, true);
                                                    //setDirty();
                                                };
//                                                }
                                            }


                                            if (q.Type == 'number' || q.Type == 'range' || q.Type == 'patient_age') {
                                                integers.push(key + '[].' + m);
                                            }

                                            if (q.Type == 'decimal') {
                                                floats.push(key + '[].' + m);
                                            }
                                        } else {
                                            qForm['onChange'] = function (modelValue, form) {
                                                //setDirty();
                                            };
                                        }

                                        // Add to array of items needed for
                                        // schema form
                                        l.items.push(qForm);
//                                        }

                                        var item = {
                                            'field': m,
                                            'label': $translate.instant(q.Label),
                                            'type': form_type[q.Type],
                                            'required': q.Required,
                                            'placeholder': $translate.instant(q.Placeholder),
                                            'choices': choices,
                                            'order': q.Order
                                        };

                                        errorMap[m] = $translate.instant(q.Label);

                                        repeating_question_items.push(item);
                                    }
                                }

                                l.items.sort(function (a, b) {
                                    return (a.order < b.order) ? -1 : (a.order > b.order) ? 1 : 0;
                                });

                                form_items.push(l);

                                //console.log(form_items);
                                //console.log(repeating_question_items);
                            }
                        }

                        if (tabs[key].Label.indexOf("print") > -1) {

                        } else {
                            tab_items.push({
                                'title': $translate.instant(tabs[key].Label),
                                'order': tabs[key].Order,
                                'items': form_items.sort(function (a, b) {
                                    return (a.order < b.order) ? -1 : (a.order > b.order) ? 1 : 0;
                                }),
                                'questions': question_items.sort(function (a, b) {
                                    return (a.order < b.order) ? -1 : (a.order > b.order) ? 1 : 0;
                                }),
                                'repeating_questions': repeating_question_items.sort(function (a, b) {
                                    return (a.order < b.order) ? -1 : (a.order > b.order) ? 1 : 0;
                                })
                            });
                        }
                    }
                }

                $scope.datetimes = datetimes;
                $scope.dates = dates;

                return tab_items.sort(function (a, b) {
                    return (a.order < b.order) ? -1 : (a.order > b.order) ? 1 : 0;
                })
            };

            $scope.get = function () {
                if (id) {

                    growl.info("LOADING_INCIDENT");

                    var tabs = questions.DashboardItems;

                    IncidentService.getStatuses()
                        .then(function (data) {
                            $scope.status_list = data.map(function (item) {
                                return {
                                    key: $translate.instant(item.key),
                                    incident_status_id: item.incident_status_id
                                };
                            });
                        });


                    if (tabs && tabs.hasOwnProperty('field_52d47aac9bd13') && tabs.field_52d47aac9bd13 && tabs.field_52d47aac9bd13.hasOwnProperty('RepeatingQuestions') && tabs.field_52d47aac9bd13.RepeatingQuestions && tabs.field_52d47aac9bd13.RepeatingQuestions.hasOwnProperty('patroller') && tabs.field_52d47aac9bd13.RepeatingQuestions.patroller) {
                        $scope.assignees = questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions.patroller.Values.map(function (item) {
                            for (var i in item) {
                                return {
                                    key: i,
                                    name: item[i]
                                };
                            }
                        });
                    } else {
                        $scope.assignees = null;
                    }

                    $scope.tabs = process_tabs(tabs);

                    // Initialize schema form to render tabs in pane
                    $scope.form = [
                        {
                            htmlClass: 'col-xs-12',
                            type: "tabs",
                            tabs: $scope.tabs
                        }
                    ];

                    growl.info("LOADING_INCIDENT");

                    // Fetches incident data base on incident ID found in url
                    IncidentService.fetch(id)
                        .then(function (data) {

                            data = JSON.parse(JSON.stringify(data), function (k, v) {
                                if (jQuery.inArray(k, floats) >= 0) {
                                    v = parseFloat(v);
                                }
                                if (jQuery.inArray(k, selects) >= 0) {
                                    v = '' + v;
                                }
                                if (jQuery.inArray(k, datetimes) >= 0) {
                                    if(v) {
                                        v = toLocalTime(v);
                                    }
                                }
                                if (jQuery.inArray(k, dates) >= 0) {
                                    if(v) {
                                        v = toLocalDate(v);
                                    }
                                }

                                return v;
                            });

                            $.each(defaults, function (k,v) {
                                if(data.hasOwnProperty(k) && (data[k] == "" || data[k] == undefined || data[k] == null)){
                                    data[k] = v;
                                }
                                else if(data.hasOwnProperty(k) && data[k] != "" && data[k] != undefined && data[k] != null){

                                }
                                else{
                                    data[k] = v;
                                }
                            });

                            $scope.incident = data;

                            if (data && data.hasOwnProperty('incident_status') && data.incident_status && data.incident_status.hasOwnProperty('incident_status_id')) {
                                $scope.incident_status = data.incident_status.incident_status_id;
                            }

                            $scope.assigned_to = data.assigned_to;

                            data.dt_created = toLocalTime(data.dt_created);

                            //will be changed to UTC when saved
                            datetimes.push("dt_created");

                            // data.photos = data.photos || [];
                            //
                            $scope.model = data;

                            $rootScope.$broadcast('schemaFormRedraw');
                            //
                            // if ($scope.has_dob) {
                            //     $scope.$watch('model.dob', function (value) {
                            //         //console.log($scope.has_age);
                            //         if (value && $scope.has_age) {
                            //             $scope.model.patient_age = calcAge(value);
                            //             //console.log("age updated");
                            //         }
                            //     });
                            // }
                        }
                        , $rootScope.on_error)
                        .finally(function () {
                            setClean();
                        });
                }
            };


            function calcAge(dateString) {
                var birthday = moment(dateString, dateFormat);
                return moment().diff(birthday, 'years');
            }

            function isEmpty(map) {
                for (var key in map) {
                    if (map.hasOwnProperty(key) && map[key] != null && map[key] !== undefined && map[key] !== "") {
                        return false;
                    }
                }
                return true;
            }

            function removeNulls(obj) {
                for (var key in obj) {

                    // value is empty string
                    if (obj[key] === '') {
                        delete obj[key];
                    }

                    // value is array with only empty strings
                    if (obj[key] instanceof Array) {
                        var empty = true;
                        for (var i = 0; i < obj[key].length; i++) {
                            if (obj[key][i] !== '') {
                                empty = false;
                                break;
                            }
                        }

                        if (empty) {
                            delete obj[key];
                        }
                    }

                    // value is object with only empty strings or arrays of empty strings
                    if (typeof obj[key] === "object") {
                        obj[key] = removeNulls(obj[key]);

                        var hasKeys = false;
                        for (var objKey in obj[key]) {
                            hasKeys = true;
                            break;
                        }

                        if (!hasKeys)
                            delete obj[key];
                    }
                }

                return obj;


                //var isArray = $.isArray(obj);
                //
                //for (var k in obj) {
                //    console.log(k);
                //    console.log(obj[k]);
                //
                //    if (obj[k] === null || obj[k] === undefined || obj[k] == "") {
                //        console.log(true);
                //        delete obj[k];
                //    }else{
                //        console.log(false);
                //    }
                //
                //    if (obj[k] && isEmpty(obj[k])) {
                //        if (isArray) {
                //            //console.log(" ==> remove from array " + k);
                //            obj.splice(k, 1)
                //        } else {
                //            //delete obj[k];
                //        }
                //    }
                //    else {
                //        if (obj[k] && typeof obj[k] == "object" && jQuery.inArray(k, repeaters) >= 0) {
                //            //console.log(k + " is repeater");
                //            removeNulls(obj[k]);
                //        }
                //    }
                //}
            }

            var transformRepeater = function (obj) {
                for (var key in obj) {

                    // value is object with only empty strings or arrays of empty strings
                    if ((jQuery.inArray(key, repeaters) >= 0) && !jQuery.isArray(obj[key])) {
                        //console.log(key + " =====" + typeof obj[key] + "======" + jQuery.isArray(obj[key]));
                        var mapValues = [];
                        angular.forEach(obj[key], function (value) {
                            mapValues.push(value);
                        });

                        obj[key] = mapValues;

                        //console.log(mapValues);
                        //console.log(obj[key]);
                    }
                }

                return obj;
            };


            $scope.save = function (form) {

                transformRepeater($scope.model);
                //console.log($scope.model);

                // First we broadcast an event so all fields validate themselves
//                $scope.$broadcast('schemaFormValidate');

                //console.log(form.$valid);

//                if (form.$valid) {

                var incident_data = JSON.parse(JSON.stringify($scope.model), function (k, v) {
//                                if (jQuery.inArray(k, floats) >= 0) {
//                                    return parseFloat(v);
//                                }
//                                if (jQuery.inArray(k, selects) >= 0) {
//                                    return '' + v;
//                                }
                    if (jQuery.inArray(k, datetimes) >= 0 && v !== '') {
                        return toUTC(v);
                    }
                    if (jQuery.inArray(k, dates) >= 0 && v !== '') {
                        return formatDate(v);
                    }


                    return v;
                });

                removeNulls(incident_data);



                var before = $scope.model;

                if (incident_data.dt_created > moment.utc().format('YYYY-MM-DD HH:mm:ss')) {
                    growl.error('INVALID_START_DATE');
                } else {

                    IncidentService
                        .saveIncident($scope.incident.incident_id, incident_data)
                        .then(function (data) {
                            growl.success("incident_updated_successfully");

                            setClean();

                            if ($scope.incident_status) {

                                if ($scope.assigned_to) {
                                    IncidentService.updateIncident(id, {
                                            "assigned_to": $scope.assigned_to + ''
                                        }
                                    ).then(function (data) {
                                            growl.info("Assignee updated");
                                        });
                                }

                                // if deleted, get confirmation
                                if ($scope.incident_status == 9) {

                                    var modalInstance = $modal.open({
                                        animation: true,
                                        templateUrl: '/app/incidents/templates/confirm.html',
                                        controller: 'ConfirmModalCtrl',
                                        size: 'md'
                                    });

                                    modalInstance.result.then(function (is_allowed) {

                                        IncidentService.updateStatus(id, {
                                                "status_type_id": $scope.incident_status + '',
                                                "status_date": toUTC(moment().format('YYYY-MM-DD HH:mm:ss')),
                                                "updated_by": currentUser.user_id
                                            }
                                        ).then(function (data) {
                                                growl.info("Status updated");
                                                $state.go('incidents');
                                            });


                                    }, function () {
                                        $log.info('Modal dismissed at: ' + new Date());
                                    });
                                } else {

                                    // else update status directly
                                    IncidentService.updateStatus(id, {
                                            "status_type_id": $scope.incident_status + '',
                                            "status_date": toUTC(moment().format('YYYY-MM-DD HH:mm:ss')),
                                            "updated_by": currentUser.user_id
                                        }
                                    ).then(function (data) {
                                            growl.info("Status updated");
                                            $state.go('incident_edit', {incidentId: $stateParams.incidentId});
                                        });
                                }
                            } else {
                                $state.go('incident_edit', {incidentId: $stateParams.incidentId});
                            }

                        }, function (error) {
                            for (var key in error) {
                                if (key in errorMap) {
                                    growl.error(errorMap[key] + " " + error[key]);
                                } else {
                                    growl.error(key + " " + error[key]);
                                }

                            }
                        });
                }
//                } else {
//                    growl.error("data_validation_error_please_correct_red_fields");
//                }
            };

            var unsavedmessage = 'All your unsaved changes will be lost. Are you sure you want to continue?';

            window.onbeforeunload = function (event) {
                if (isDirty()) {
                    var message = unsavedmessage;

                    var event = event || window.event;

                    if (event) {
                        event.returnValue = message;
                    }
                    else {
                        return message;
                    }
                }
            };

            $scope.$on('$destroy', function () {
                //console.log($scope.incidentform.$dirty);
//                console.log('$destroy');
                window.onbeforeunload = null;
            });

            $scope.$on('$stateChangeStart', function (event, next, current) {
//                console.log('$stateChangeStart');
//                console.log($scope.incidentform.$dirty);

                if (isDirty()) {
                    if (!confirm(unsavedmessage)) {
                        event.preventDefault();
                    }
                }
            });

            $scope.gotoNextTab = function () {
                var scope = jQuery('.schema-form-tabs').scope();

                if (scope && scope.hasOwnProperty('selected')) {
                    var currentTab = scope.selected.tab;
                    if (currentTab == ($scope.tabs.length - 1)) {
                        scope.selected.tab = 0;
                    } else {
                        scope.selected.tab++;
                    }

                    $("html, body").animate({scrollTop: 0}, 200);
                }
            };

        }]);
