'use strict';

ShassaroApp.controller('LoginController', function ($scope, $rootScope, $modalInstance, AUTH_EVENTS, AuthenticationService) {
    $scope.credentials = {
        username: '',
        password: ''
    };

    $scope.tryLogin = function () {
        AuthenticationService.login($scope.credentials).success(
            function () {
                $modalInstance.close(true);
            },
            function () {
                $scope.authenticationFailed = true;
            });
    };
});