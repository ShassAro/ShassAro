'use strict';

ShassaroApp.controller('RegisterController', function ($scope, $modalInstance, $timeout, AuthenticationService, Users) {
    $scope.registration = {
        username: '',
        password: '',
        verifyPassword: '',
        email: '',
        first_name: '',
        last_name: ''
    };

    $scope.tryRegister = function () {
        var request = AuthenticationService.register($scope.registration);
        request.success(function () {
            $scope.registrationSucceded = true;
            var credentials = {username: $scope.registration.username, password: $scope.registration.password};
            AuthenticationService.login(credentials).
                success(function () {
                    $modalInstance.close(true);
                });
        });

        request.error(function () {
            $scope.registrationFailed = true;
        });
    };

    $scope.usernameExist = false;
    $scope.validateUserNameExist = function () {
        if($scope.registration.username == null || $scope.registration.username == '') return;
        Users.query().$promise
            .then(function (users) {
                $scope.usernameExist = users.some(function (user) {return user.username == $scope.registration.username;});
            })
            .catch(function () {$scope.usernameExist = false;});
    };

    $scope.emailExist = false;
    $scope.validateEmailExist = function () {
        if($scope.registration.email == null || $scope.registration.email == '') return;
        Users.query().$promise.
            then(function (users) {
                $scope.emailExist = users.some(function (user) {return user.email == $scope.registration.email;});
            });
    };

    $scope.closeRegisterOpenLogin = function () {
        $modalInstance.close('show-login');
    }
});