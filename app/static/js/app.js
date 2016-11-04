
var musicApp = angular.module('musicApp', []);


// Controller for about page
musicApp.controller('musicController', function musicController($scope, $http) {
    $scope.runTests = function() {
        $scope.showTestsOutput = true;
        $scope.testOutput = '\nPlease wait for the tests... '
        $http.get('/run_unittests').then(function(result){
            $scope.finished = true;
            $scope.testOutput = '\n' + result;
        });
        //return ($scope.testOutput); // it gets back through testOutput instead
    }
});
