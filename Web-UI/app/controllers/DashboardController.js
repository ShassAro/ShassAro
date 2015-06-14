'use strict';

ShassaroApp.controller('DashboardController', function ($scope, Users, Session, GameResults) {
    $scope.user = Session.user;
    $scope.stats = Users.stats({username: $scope.user.username});
    $scope.gameResults = [];
    $scope.totalExperience = 0;

    GameResults.specificUserWinnings({username:$scope.user.username}).$promise.then(function (gameResults) {
        function userDisplayName(user) {
            return user.first_name + ' ' + user.last_name;
        }

        for (var i in gameResults) {
            var result = gameResults[i];
            try{
                $scope.gameResults.push({
                    opponentName: userDisplayName(result.losing_users[0]),
                    opponentEmail: result.losing_users[0].email,
                    startTime: result.start_time,
                    win: true,
                    experience: result.experience_gained
                });
                $scope.totalExperience += result.experience_gained;
            }
            catch(e){}
        }
    });

    GameResults.specificUserLosings({username:$scope.user.username}).$promise.then(function (gameResults) {
        function userDisplayName(user) {
            return user.first_name + ' ' + user.last_name;
        }

        for (var i in gameResults) {
            var result = gameResults[i];
            try{
                $scope.gameResults.push({
                    opponentName: userDisplayName(result.winning_users[0]),
                    opponentEmail: result.winning_users[0].email,
                    startTime: result.start_time,
                    win: false,
                    experience: 0
                });
            }
            catch(e){}
        }
    });

    //GameResults.query().$promise.then(function (gameResults) {
    //    gameResults = gameResults.sort(function (a, b) {
    //        return -(new Date(a.start_time) - new Date(b.start_time));
    //    });
    //
    //    for(var i in gameResults) {
    //        var result = gameResults[i];
    //        if(!angular.isDefined(result.pk)) continue;
    //        if (result.winning_users.some(function (user) {
    //                return user.username == $scope.user.username;
    //            })) {
    //            $scope.gameResults.push({
    //                opponentName: result.losing_users[0].first_name + ' ' + result.losing_users[0].last_name,
    //                opponentEmail: result.losing_users[0].email,
    //                startTime: result.start_time,
    //                win: true,
    //                experience: result.experience_gained
    //            });
    //            $scope.totalExperience += result.experience_gained;
    //        }
    //        else if (result.losing_users.some(function (user) {
    //                return user.username == $scope.user.username;
    //            })) {
    //            $scope.gameResults.push({
    //                opponentName: result.winning_users[0].first_name + ' ' + result.winning_users[0].last_name,
    //                opponentEmail: result.winning_users[0].email,
    //                startTime: result.start_time,
    //                win: false,
    //                experience: 0
    //            });
    //        }
    //    }
    //});
});