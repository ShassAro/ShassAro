'use strict';

ShassaroApp.controller('ApplicationController', function ($scope, $rootScope, AUTH_EVENTS, Session) {
    $scope.currentUser = null;
    $scope.watchUser = {};

    $rootScope.$on(AUTH_EVENTS.loginSuccess, function (event, data) {
        $scope.setCurrentUser(data);
    });

    $rootScope.$on(AUTH_EVENTS.logoutSuccess, function (event, data) {
        $scope.setCurrentUser(null);
    });

    $scope.setCurrentUser = function (user) {
        $scope.currentUser = user;
        $scope.watchUser.user = user;
    };

    Session.tryRestore();
});

ShassaroApp.run(function ($rootScope, AUTH_EVENTS, AuthenticationService) {
    //$rootScope.$on('$routeChangeStart', function (event, next) {
    //    if(!AuthenticationService.isAuthenticated()){
    //        event.preventDefault();
    //        $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
    //    }
    //});
});

ShassaroApp.config(function ($httpProvider) {
    $httpProvider.interceptors.push(['$injector', function ($injector) {
        return $injector.get('AuthenticationInterceptor');
    }]);
});

ShassaroApp.factory('AuthenticationInterceptor', function ($rootScope, $q, AUTH_EVENTS) {
    return {
        responseError: function (response) {
            $rootScope.$broadcast({
                401: AUTH_EVENTS.notAuthenticated,
                403: AUTH_EVENTS.notAuthenticated
            }[response.status], response);

            return $q.reject(response);
        }
    }
});

ShassaroApp.directive('loginDialog', function (AUTH_EVENTS) {
    return {
        restrict: 'A',
        template: '<div ng-if="visible" ng-include="\'views/Login.html\'">',
        link: function (scope) {
            var showDialog = function () {
                scope.visible = true;
            };

            scope.visible = false;
            scope.$on(AUTH_EVENTS.notAuthenticated, showDialog);
            scope.$on(AUTH_EVENTS.sessionTimeout, showDialog);
        }
    }
});