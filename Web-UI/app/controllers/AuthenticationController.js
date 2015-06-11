'use strict';

ShassaroApp.controller('AuthenticationController', function ($scope, $rootScope, $modal, $timeout, AUTH_EVENTS, AuthenticationService) {
    $scope.firstTimeNotAuthenticated = true;
    $rootScope.$on(AUTH_EVENTS.notAuthenticated, function (event, data) {
        $scope.shouldLogin();
    });
    $rootScope.$on(AUTH_EVENTS.sessionTimeout, function () {
        $scope.shouldLogin();
    });

    $scope.shouldLogin = function () {
        if($scope.firstTimeNotAuthenticated){
            $timeout(function () {
                if($scope.currentUser) return;
                $scope.openLoginModal();
            },1000)
        }
    };

    $scope.afterUserIsLoggedIn = function () {
        $scope.isAuthenticated = true;
        $scope.user = ShassaroApp.user;

        //$location.path('/dashboard');
    };

    $scope.afterUserIsLoggedOut = function () {
        delete $scope.isAuthenticated;
        //$location.path('/');
    };

    $scope.openLoginModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Login.html',
            controller: 'LoginController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn){
                $scope.afterUserIsLoggedIn();
            }
        });
    };

    $scope.openRegisterModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Register.html',
            controller: 'RegisterController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn)
                $scope.afterUserIsLoggedIn();
        });
    };

    $scope.logout = function () {
        AuthenticationService.logout().success(function () {
            $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
        });
    };
});

ShassaroApp.controller('AuthenticationController_OLD', function ($scope, $location, $modal, AuthenticationService, Users) {
    //$scope.$evalAsync(function () {
    //    AuthenticationService.isAuthenticated().true(function () {
    //        $scope.$apply(function () {
    //            $scope.isAuthenticated = true;
    //        });
    //    })
    //});
    //$scope.$watch('isAuthenticated', function (isAuthenticated) {
    //    if(isAuthenticated) {
    //        $scope.afterUserIsLoggedIn();
    //    }
    //});

    $scope.$on(AUTH_EVENTS.notAuthenticated, $scope.openLoginModal);
    $scope.$on(AUTH_EVENTS.sessionTimeout, $scope.openLoginModal);

    $scope.afterUserIsLoggedIn = function () {
        $scope.isAuthenticated = true;
        $scope.user = ShassaroApp.user;

        //$location.path('/dashboard');
    };

    $scope.afterUserIsLoggedOut = function () {
        delete $scope.isAuthenticated;
        //$location.path('/');
    };

    $scope.openLoginModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Login.html',
            controller: 'LoginController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn){
                $scope.afterUserIsLoggedIn();
            }
        });
    };

    $scope.openRegisterModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'views/Register.html',
            controller: 'RegisterController'
        });

        modalInstance.result.then(function (loggedIn) {
            if(loggedIn)
                $scope.afterUserIsLoggedIn();
        });
    };

    $scope.logout = function () {
        AuthenticationService.logout().success(function () {
            $scope.afterUserIsLoggedOut();
        });
    };
});

ShassaroApp.controller('LoginController', function ($scope, $rootScope, $modalInstance, AUTH_EVENTS, AuthenticationService) {
    $scope.credentials = {
        username: '',
        password: ''
    };

    $scope.tryLogin = function () {
        AuthenticationService.login($scope.credentials).success(
            function (response) {
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess, response.user);
                $modalInstance.close(true);
            },
            function () {
                //$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
                $scope.authenticationFailed = true;
            });
    };
});

ShassaroApp.controller('RegisterController', function ($scope, $modalInstance, $timeout, AuthenticationService, Users) {
    $scope.username='';
    $scope.password ='';
    $scope.verifyPassword='';
    $scope.email = '';
    $scope.first_name = '';
    $scope.last_name = '';

    $scope.tryRegister = function () {
        var request = AuthenticationService.register($scope.username, $scope.password, $scope.first_name, $scope.last_name, $scope.email);
        request.success(function () {
            $scope.registrationSucceded = true;
            AuthenticationService.login($scope.username, $scope.password).
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
        if($scope.username == null || $scope.username == '') return;
        Users.query().$promise
            .then(function (users) {
                $scope.usernameExist = users.some(function (user) {return user.username == $scope.username;});
            })
            .catch(function () {$scope.usernameExist = false;});
    };

    $scope.emailExist = false;
    $scope.validateEmailExist = function () {
        if($scope.email == null || $scope.email == '') return;
        Users.query().$promise.
            then(function (users) {
                $scope.emailExist = users.some(function (user) {return user.email == $scope.email;});
            });
    }
});