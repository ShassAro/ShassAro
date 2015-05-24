'use strict';

ShassaroApp.controller('LoginController', function ($scope, $location, LoginService, $modal) {
    $scope.openModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Login.html',
            controller: 'LoginModalController'
        });
    }
});

ShassaroApp.controller('LoginModalController', function ($scope, $modalInstance) {
    $scope.isAuthenticated = false;
    $scope.username = '';
    $scope.password = '';

    $scope.tryLogin = function () {
        LoginService.login($scope.username, $scope.password).
            success(function () {
                document.location = '/Shassaro/app/';
            }).
            error(function () {
                console.error(arguments);
            });
    };
});