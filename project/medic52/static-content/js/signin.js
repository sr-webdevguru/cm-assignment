var app = angular.module('SigninApp', ['ngMaterial']);

app.controller('AppCtrl', ['$scope', function($scope) {
    $scope.login = function(){
        angular.element(document.querySelector('#login-form')).submit();
    }
}]);