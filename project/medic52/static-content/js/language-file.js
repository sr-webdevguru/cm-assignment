var app = angular.module('StarterApp', ['ngMaterial','ngFileUpload']);

app.controller('AppCtrl', ['$scope', '$mdDialog', 'Upload', function($scope, $mdDialog, Upload){
  var alert;
  $scope.uploadStatus = false;
  $scope.showDialog = function($event) {
    alert = $mdDialog.alert({
      title: 'Attention',
      content: 'This is an example of how easy dialogs can be!',
      ok: 'Close'
    });

    $mdDialog
        .show( alert )
        .finally(function() {
          alert = undefined;
        });
  };

  $scope.upload = function (files) {
    $scope.uploadStatus = true;
    if (files && files.length) {
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        Upload.upload({
          url: location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '')+'/api/v3/upload/lang/',
          file: file
        })
        .success(function (data, status, headers, config) {
              $scope.uploadStatus = false;
          var upload_alert = $mdDialog.alert({
            title: 'Success',
            content: data,
            ok: 'Close'
          });
          $mdDialog
          .show( upload_alert )
          .finally(function() {
            alert = undefined;
          });
        });
      }
    }
  };
}]);