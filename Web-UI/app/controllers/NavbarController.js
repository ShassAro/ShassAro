'use strict';

ShassaroApp.controller('NavbarController', function ($scope) {
    $scope.isUserAuthenticated = function () {
        return ShassaroApp.user != null;
    }
});