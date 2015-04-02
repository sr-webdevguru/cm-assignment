'use strict';


angular.module('app')
    .controller('StockCheckoutCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'StockService', 'UserService', 'currentUser', 'controlledSubstances', 'locations', 'questions', 'growl', function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, StockService, UserService, currentUser, controlledSubstances, locations, questions, growl) {

        initialize();

        $scope.checkout = function () {
            growl.info("CHECKOUT_ASSET");

            StockService.checkout($scope.controlled_substance_stock.controlled_substance_stock_id, $scope.user_id).then(function (data) {
                    growl.success("stock_checkout_successfully");
                    //$state.go("stock_report");
                },
                function (error) {
                    growl.error(error.detail);

                    //Global errors
                    //if (error.hasOwnProperty('detail')) {
                    //    $scope.error = error.detail;
                    //    $scope.form.$setPristine();
                    //    growl.error(error.detail);
                    //}
                    //
                    //$scope.errors = [];
                    //angular.forEach(error, function (errors, field) {
                    //
                    //    if (field == 'non_field_errors') {
                    //        // Global errors
                    //        $scope.error = errors.join(', ');
                    //        $scope.form.$setPristine();
                    //    } else {
                    //        //Field level errors
                    //        $scope.form[field].$setValidity('backend', false);
                    //        $scope.form[field].$dirty = true;
                    //        $scope.errors[field] = errors.join(', ');
                    //    }
                    //});
                });
        };

        function initialize() {
            $scope.controlled_substances = controlledSubstances.results;
            $scope.controlled_substance = {};
            $scope.controlled_substance.controlled_substance_id = '';

            $scope.locations = locations.results;

            $scope.$watch('location_id', function (newValue, oldValue) {
                if (newValue && newValue != oldValue) {
                    //console.log("location watched");
                    updateStock($scope.location_id, $scope.controlled_substance.controlled_substance_id);
                }
            });

            $scope.$watch('controlled_substance', function (newValue, oldValue) {
                if (newValue && newValue != oldValue) {
                    //console.log("substance watched");
                    updateStock($scope.location_id, $scope.controlled_substance.controlled_substance_id);
                }
            });

            if ($stateParams.hasOwnProperty('controlledSubstanceId')) {
                $scope.controlled_substance = _.find(controlledSubstances.results, function (controlledSubstance) {
                    return controlledSubstance.controlled_substance_id == $stateParams.controlledSubstanceId;
                })
            }

            if ($stateParams.hasOwnProperty('locationId')) {
                $scope.location_id = $stateParams.locationId;
            }

            if ($scope.controlled_substance) {
                updateStock($scope.location_id, $scope.controlled_substance.controlled_substance_id);
            }

            fetchUsers();

        }

        function fetchUsers() {
            var tabs = questions.DashboardItems;

            if (tabs && tabs.hasOwnProperty('field_52d47aac9bd13') && tabs.field_52d47aac9bd13 && tabs.field_52d47aac9bd13.hasOwnProperty('RepeatingQuestions') && tabs.field_52d47aac9bd13.RepeatingQuestions && tabs.field_52d47aac9bd13.RepeatingQuestions.hasOwnProperty('patroller') && tabs.field_52d47aac9bd13.RepeatingQuestions.patroller) {
                $scope.users = questions.DashboardItems.field_52d47aac9bd13.RepeatingQuestions.patroller.Values.map(function (item) {
                    for (var i in item) {
                        return {
                            key: i,
                            name: item[i]
                        };
                    }
                });

            } else {
                $scope.users = null;
            }

//            UserService.fetchAll(1000, 1).then(function (data) {
//                $scope.users = data.results.map(function (item) {
//                        return {
//                            key: item.user_id,
//                            name: item.name
//                        };
//
//                });
//            }, function (error) {
//                $scope.users = null;
//            })
        }

        function updateStock(locationId, controlledSubstanceId) {
            StockService.fetchAll(1000, 1, '', 'controlled_substance__controlled_substance_name', false, 'in', locationId, controlledSubstanceId, null, null)
                .then(function (data) {
                    var controlled_substance_stocks = data.results.map(function (stock) {
                        stock.controlled_substance_stock_text = stock.controlled_substance_stock_pk + " (" + stock.volume + " " + stock.controlled_substance.units + ")";
                        return stock;
                    });

                    $scope.controlled_substance_stocks = controlled_substance_stocks;

                    if ($stateParams.hasOwnProperty('controlledSubstanceStockId')) {
                        $scope.controlled_substance_stock = _.find(controlled_substance_stocks, function (controlledSubstanceStock) {
                            return controlledSubstanceStock.controlled_substance_stock_id == $stateParams.controlledSubstanceStockId;
                        })
                    }
                },
                function (error) {
                    growl.error(error.detail);
                }
            );
        }
    }]);
