angular.module('app.services')
    .service('QuestionService', ['$http', '$q', '$log', '$rootScope', '$window', 'LS', 'CONFIG','ApiService', function ($http, $q, $log, $rootScope, $window, LS, CONFIG, ApiService) {

        var currentUser = JSON.parse(LS.get('user'));
//        $log.log(currentUser);

        var resort_id= currentUser.resorts[0].resort_id;
//        $log.log(resort_id);


        var service = {
            fetch: function () {
                var d = $q.defer();

                    $http.get(ApiService.base() + CONFIG.API_URL + '/incidents/config/', {
                        params:{
                            resort_id: resort_id
                        }
                    })
                        .success(function (response, status, headers) {

                            d.resolve(response);
                        })
                        .error(function (response, status, headers, config, errors) {
                            d.reject(response);
                        });

                    return d.promise;
//                }


            }
        };

        return service;
    }]);

