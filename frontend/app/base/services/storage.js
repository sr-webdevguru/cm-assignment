angular.module('app').factory("LS", function ($window, $rootScope) {
    angular.element($window).on('storage', function (event) {
        if (event.key === 'use') {
            $rootScope.$apply();
        }
    });
    return {
        set: function (key, val) {
            $window.localStorage && $window.localStorage.setItem(key, val);
            return this;
        },
        get: function (key) {
            return $window.localStorage && $window.localStorage.getItem(key);
        },
        clear: function() {
            $window.localStorage.clear();
            return true
        }
    };
});