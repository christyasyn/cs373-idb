
var mainApp = angular.module('iMusicDB', ['ngRoute' , 'ngAnimate', 'ui.bootstrap']);


// Controller for about page
mainApp.controller('aboutCtrl', function($scope, $http) {
    $scope.runTests = function() {
        $scope.showTestsOutput = true;
        $scope.testOutput = '\nPlease wait for the tests... '
        $http.get('/run_unittests').then(function(result){
            $scope.finished = true;
            $scope.testOutput = '\n' + result.data.output;
        });
    }
});
