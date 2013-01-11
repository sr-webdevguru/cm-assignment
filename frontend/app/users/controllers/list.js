'use strict';


angular.module('app')
    .controller('UserListCtrl', function ($scope, $location, $state, $rootScope, $timeout, $log, $intercom, UserService, currentUser, growl) {

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
            dashboard_feature_last_used: "Users"
        });

        if (!UserService.currentUser().isManager) {
            $state.go("map");
        }


        $scope.list = {
            users: [],
            filtered: [],
            currentPage: 1,
            itemsPerPage: 20,
            totalItems: 0,
            totalPages: 0,
            predicate: 'user__name',
            loading: false,

            setPage: function (pageNum) {
                $scope.list.currentPage = pageNum;
            },

            filter: function () {
                $timeout(function () {
                    $scope.list.filteredItems = $scope.list.filtered.length;
                    $scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }, 10);
            },

            sort_by: function (predicate) {
                $scope.list.predicate = predicate;
                $scope.list.reverse = !$scope.list.reverse;

                $scope.list.get();
            },

            get: function () {
                $log.log('fetching users...');
                $scope.list.loading = true;

                growl.info("LOADING_USER");
                UserService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, '', $scope.list.predicate, $scope.list.reverse )
                    .then(function (data) {
                        $scope.list.loading = false;

                        $scope.list.users = data.results;
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);
                    },
                    $rootScope.on_error
                );
            },

            search: function (text) {
                $scope.list.loading = true;

                growl.info("LOADING_USER");

                UserService.fetchAll($scope.list.itemsPerPage, $scope.list.currentPage, text, $scope.list.predicate, $scope.list.reverse)
                    .then(function (data) {
                        $scope.list.loading = false;

                        $scope.list.users = data.results;
                        $scope.list.totalItems = data.count;
                        $scope.list.totalPages = Math.ceil($scope.list.totalItems / $scope.list.itemsPerPage);
                    },
                    $rootScope.on_error
                );
            }
        };

        $scope.add = function () {
            $state.go("user_add");
        };

        $scope.$watch(
            'list.itemsPerPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        $scope.$watch(
            'list.currentPage',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    $scope.list.get();
                    //$scope.list.totalPages = Math.ceil($scope.list.filteredItems / $scope.list.itemsPerPage);
                }
            }
        );

        var filterTextTimeout;

        $scope.$watch(
            'search',
            function (newValue, oldValue) {
                if (newValue !== oldValue) {

                    if (filterTextTimeout) {
                        $timeout.cancel(filterTextTimeout);
                    }

                    filterTextTimeout = $timeout(function () {
                        console.log("value changed");
                        $scope.list.search(newValue);
                    }, 1000); // delay 250 ms


                }
            }
        );

    });


