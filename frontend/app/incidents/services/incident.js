angular.module('app.services')
    .service('IncidentService', ['$http', '$q', '$log', 'UserService', 'LS',  'CONFIG', 'ApiService', function ($http, $q, $log, UserService, LS, CONFIG, ApiService) {

        var API = {
            base:  CONFIG.API_URL + '/incidents/',
            getUrl: function (id) {
                return '/' + id;
            }
        };

        return {
//            _user : null,

            fetchAll: function (dateFrom, dateTo, resort_id, chunk, page) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base, {
                    params: {
                        resort_id: resort_id,
                        date_from: dateFrom,
                        date_to: dateTo,
                        chunk: chunk,
                        offset: (page - 1) * chunk
                    }
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchList: function (dateFrom, dateTo, resort_id, chunk, page, predicate, direction) {
                var d = $q.defer();

                predicate = predicate || 'dt_created';

                $http.get(ApiService.base() + API.base, {
                    params: {
                        resort_id: resort_id,
                        date_from: dateFrom,
                        date_to: dateTo,
                        chunk: chunk,
                        offset: (page - 1) * chunk,
                        order_by:predicate,
                        order_by_direction: direction ? 'desc':'asc'
                    }
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchReport: function (dateFrom, dateTo, chunk, page, model, resort_id, format) {
                var d = $q.defer();

                var params = {
                        datefrom: dateFrom,
                        dateto: dateTo,
                        resort_id: resort_id,
                        chunk: chunk,
                        offset:(page - 1) * chunk,
                        output_format: format
                    };

                var filters = {};

                angular.forEach(model, function(value, key) {
                    if(value && value.field && value.field.fullkey) {
                        filters[value.field.fullkey] = filters[value.field.fullkey] || [];
                        filters[value.field.fullkey].push(value.value);

                        if(value.hasOwnProperty('childField') && value.childField.value && (value.childField.value != 'all')){
                            filters[value.childField.field.fullkey] = filters[value.childField.field.fullkey] || [];
                            filters[value.childField.field.fullkey].push(value.childField.value);
                        }
                    }
                });

                $http({
                    method: 'POST',
                    url: ApiService.base() + CONFIG.API_URL + '/reports/table/',
                    params: params,
                    data:filters
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchChart: function (model, chart, resort_id) {
                var d = $q.defer();

                var params = {
                        resort_id: resort_id
                    };

                $http({
                    method: 'POST',
                    url: ApiService.base() + CONFIG.API_URL + '/reports/'+chart+'/',
                    params: params,
                    data:model
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchChartCSV: function (model, chart, resort_id, format) {
                var d = $q.defer();

                var params = {
                        resort_id: resort_id,
                        output_format: format
                    };

                $http({
                    method: 'POST',
                    url: ApiService.base() + CONFIG.API_URL + '/reports/'+chart+'/',
                    params: params,
                    data:model
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchStatusReport: function (dateFrom, dateTo, status_list, chunk, page, output_format) {
                var d = $q.defer();

                $http.get(ApiService.base() + CONFIG.API_URL + '/reports/status/', {
                        params: {
                            datefrom: dateFrom,
                            dateto: dateTo,
                            chunk: chunk,
                            offset: (page - 1) * chunk,
                            status: status_list,
                            output_format: output_format
                        }
                    })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetch: function (id) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base + id + '/')
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            fetchMap: function (dateFrom, dateTo, resort_id, chunk, page) {
                var d = $q.defer();

                $http.get(ApiService.base() + API.base, {
                    params: {
                        resort_id: resort_id,
                        date_from: dateFrom,
                        date_to: dateTo,
                        chunk: chunk,
                        offset: (page - 1) * chunk,
                        include_status: "1,2,3,4,5,6,7"
                    }
                })
                    .success(function (response, status, headers) {
                        d.resolve(response);
                    })
                    .error(function (response, status, headers, config, errors) {
                        d.reject(response);
                    });

                return d.promise;
            },

            print: function (id) {
                var data = {
                    'id': id || ''
                };

                var d = $q.defer();

                $http.get(ApiService.base() + API.base + API.getUrl(data.id) + '/print/')
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            fetchNotes: function (id) {
                var data = {
                    'id': id || ''
                };

                var d = $q.defer();

                $http.get(ApiService.base() + API.base + id + '/notes/')
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            addNote: function (incident_id, note, time) {
                //var data = {
                //    'id': id || ''
                //};

                var params = {
                    //'note_id': '',
                    'field_52ca448dg94ja3': note,
                    'field_52ca448dg94ja4': time
                };

                var d = $q.defer();

                $http.post(ApiService.base() + API.base + incident_id + '/notes/', params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            getStatuses: function () {
                //var data = {
                //    'id': id || ''
                //};

//                var params = {
//                };

                var d = $q.defer();

                $http.get(ApiService.base() + API.base + 'status/')
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },


            saveNote: function (id, note_id, note) {
                //var data = {
                //    'id': id || ''
                //};

                var params = {
                    //'note_id': '',
                    'content': note,
                    'note_date': new Date()
                };

                var d = $q.defer();

                $http.post(ApiService.base() + API.base + id + '/notes/', params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            saveIncident: function (id, incidentData) {
                var data = {
                    'id': id || ''
                };

                var params = {
                    'data': incidentData
                };

                var d = $q.defer();

                $http.put(ApiService.base() + API.base + id + '/', incidentData)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            createIncident: function (incidentData) {
                //var data = {
                //    'id': id || ''
                //};
                //
                //var params = {
                //    'data': incidentData
                //};

                var params = incidentData || {};

                var d = $q.defer();

                $http.post(ApiService.base() + API.base, params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            updateStatus: function (id, incidentData) {

                var params = incidentData || {};

                var d = $q.defer();

                $http.post(ApiService.base() + API.base + id + '/status/', params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            },

            updateIncident: function (id, incidentData) {

                var params = incidentData || {};

                var d = $q.defer();

                $http.put(ApiService.base() + API.base + id + '/', params)
                    .success(function (data, status, headers) {
                        d.resolve(data);
                    })
                    .error(function (data, status, headers, config, errors) {
                        d.reject(data);
                    });

                return d.promise;
            }

            //updateLocation: function (id, incidentData) {
            //
            //    var params = incidentData || {};
            //
            //    var d = $q.defer();
            //
            //    $http.put(ApiService.base() + API.base + id + '/', params)
            //        .success(function (data, status, headers) {
            //            d.resolve(data);
            //        })
            //        .error(function (data, status, headers, config, errors) {
            //            d.reject(data);
            //        });
            //
            //    return d.promise;
            //}
        };

//        return service;
    }]);

