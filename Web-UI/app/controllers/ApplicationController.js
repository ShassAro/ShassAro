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