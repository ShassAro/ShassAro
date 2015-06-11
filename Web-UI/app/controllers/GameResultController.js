'use strict';

ShassaroApp.controller('GameResultController', function ($scope, ActiveGames, GameResults, $http) {
    $scope.gameTags = [];
    ActiveGames.get({username: $scope.currentUser.username}).$promise.then(function (response) {
        GameResults.get({id: response.id}).$promise.then(function (gameResult) {
            $scope.userWon = gameResult.winning_users.some(function(user){ return user.username == $scope.currentUser.username });
            $scope.gameResult = gameResult;
            delete $scope.gameResult.winning_users;
            delete $scope.gameResult.losing_users;
            for(var i in $scope.gameResult.tags){
                var tagUrl = $scope.gameResult.tags[i];
                $http.get(tagUrl).success(function (tag) {
                    $scope.gameTags.push(tag.name);
                });
            }
        });
    });
});