'use strict';

ShassaroApp.controller('LoginController', function ($scope, $location, $modal) {
    $scope.openModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Login.html',
            controller: 'LoginModalController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn){
                $scope.isAuthenticated = true;
            }
        });
    }
});

ShassaroApp.controller('LoginModalController', function ($scope, $modalInstance, LoginService) {
    $scope.username = '';
    $scope.password = '';

    $scope.tryLogin = function () {
        $modalInstance.close(true);

        LoginService.login($scope.username, $scope.password).
            success(function () {
                $modalInstance.close(true);
            }).
            error(function () {
                $scope.authenticationFailed = true;
            });
    };
});