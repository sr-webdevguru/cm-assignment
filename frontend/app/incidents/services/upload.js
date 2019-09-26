// Call parent module reference
angular.module('app.services')

    .service('UploadService',
    ['$http',
        '$q',
        'CONFIG',
        'LS',
        'ApiService',
        function ($http, $q, CONFIG, LS, ApiService) {


            var API_UPLOAD = CONFIG.API_URL + '/incidents/{id}/media/';

            return {
                /*
                 @params incidentId - The incident Id
                 @params type - The file type to upload (image || file)
                 */
                upload: function (incidentId, formData, type) {
                    var dfd = $q.defer(),
                        xhr = new XMLHttpRequest(),

                        onProgress = function (event) {
                            dfd.notify(event);
                        },

                        onFinish = function (event) {
                            var responseText = event.target.responseText,
                                source;

                            if (event.target.status == '200' && responseText) {
                                try {
                                    source = JSON.parse(responseText);

                                    dfd.resolve(source);
                                } catch (error) {
                                    dfd.reject(event.target);
                                }
                            } else {
                                onError(event.target);
                            }
                        },

                        onError = function (error) {
                            dfd.reject(error);
                        },

                        url = ApiService.base() + API_UPLOAD.replace('{id}', incidentId);

                    xhr.upload.onprogress = onProgress;
                    xhr.addEventListener('loadend', onFinish, false);

                    // Set up request
                    xhr.open('POST', url, true);

                    var authorization = LS.get('Authorization');
                    var token = LS.get('token');

                    if (authorization != null) {
                        xhr.setRequestHeader('Authorization', authorization);
                    }

                    if (token != null) {
                        xhr.setRequestHeader('token', token);
                    }

                    xhr.setRequestHeader('Accept', 'application/json');

                    // Fire!
                    xhr.send(formData);

                    return dfd.promise;
                }
            }
        }]);