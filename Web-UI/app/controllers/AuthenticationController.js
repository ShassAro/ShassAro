'use strict';

ShassaroApp.controller('AuthenticationController', function ($scope, $rootScope, $modal, $location, $timeout, AUTH_EVENTS, AuthenticationService) {
    $scope.firstTimeNotAuthenticated = true;
    $rootScope.$on(AUTH_EVENTS.notAuthenticated, function (event, data) {
        $scope.shouldLogin(data);
    });
    $rootScope.$on(AUTH_EVENTS.sessionTimeout, function () {
        $scope.shouldLogin();
    });

    $scope.shouldLogin = function (redirectToPath) {
        if($scope.firstTimeNotAuthenticated){
            $timeout(function () {
                if($scope.currentUser) return;
                $scope.openLoginModal(redirectToPath);
            },1000)
        }
    };

    $scope.afterUserIsLoggedIn = function (redirectToPath) {
        $scope.isAuthenticated = true;
        if(angular.isString(redirectToPath)){
            $location.path(redirectToPath);
        }
        else if($location.path() == '/'){
            $location.path('/dashboard');
        }
    };

    $scope.openLoginModal = function (redirectToPath) {
        var modalInstance = $modal.open({
            templateUrl: 'views/Login.html',
            controller: 'LoginController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn){
                $scope.afterUserIsLoggedIn(redirectToPath);
            }
        });
    };

    $scope.openRegisterModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Register.html',
            controller: 'RegisterController'
        });

        modalInstance.result.then(function (result) {
            if(angular.isString(result) && result == 'show-login'){
                $scope.openLoginModal();
            }
            else if(result === true) {
                $scope.afterUserIsLoggedIn();
            }
        });
    };

    $scope.logout = function () {
        AuthenticationService.logout().success(function () {
            $location.path('/');
        });
    };
});