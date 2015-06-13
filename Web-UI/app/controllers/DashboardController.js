'use strict';

ShassaroApp.controller('DashboardController', function ($scope, Users, Session) {
    $scope.user = Session.user;
    $scope.stats = Users.stats({username: $scope.user.username});
});