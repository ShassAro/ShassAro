'use strict';

ShassaroApp.controller('GameController', function ($scope, $websocket, $interval, user, ActiveGames, Users) {
    //var socket = $websocket(ShassaroApp.api_host_url.replace('http://','ws://')+'/ws/'+user.username+'-game?subscribe-broadcast');
    //socket.onMessage(function (event) {
    //    if(angular.isObject(event.data)){
    //        // handle active game object
    //        var activeGame = event.data;
    //        $scope.opponentGoalsCompleted = activeGame.remote_goals_count;
    //    }
    //    else{
    //        // handle a redirect
    //        var gameResultUrl = event.data;
    //    }
    //    var gameInfo = JSON.parse(event.data);
    //    console.log(gameInfo);
    //});

    App.sidebar('close-sidebar');

    $scope.isConnected = false;
    $scope.username = user.username;
    $scope.gameCompleted = false;

    $scope.getOpponentGoalsCount = function () {
        return Array($scope.opponentGoalsCompleted);
    };

    ActiveGames.get({username: $scope.username}).$promise
        .then(function (gameInfo) {
            $scope.vncHost = gameInfo.docker_manager_ip;
            $scope.vncPort = gameInfo.vnc_port;
            $scope.vncPassword = gameInfo.password;
            $scope.goals = [];
            if(angular.isDefined(gameInfo.goals)) {
                for (var i = 0; i < gameInfo.goals.length; i++) {
                    $scope.goals.push({description: gameInfo.goals[i], hint: gameInfo.hints[i]});
                }
            }
            $scope.opponentIP = gameInfo.remote_ip;
            Users.get({username: gameInfo.remote_username}).$promise.then(function (user) {
                $scope.opponentUsername = user.username;
                $scope.opponentMail =  user.email;
                $scope.opponentDisplayName = user.first_name + ' ' + user.last_name;
            });
            $scope.opponentGoalsCompleted = gameInfo.remote_goals_count;
            $scope.isConnected = true;

            $scope.gameStartTime = new Date(gameInfo.start_time);
            $scope.gameEndTime = $scope.gameStartTime.addMinutes(gameInfo.duration).getTime();
            $scope.gameStartTime = $scope.gameStartTime.getTime();
        })
        .catch(function () {
           $scope.dockerConnectionError = true;
        });


    $scope.verifyGoal = function (goal) {
        goal.invoked = true;
        ActiveGames.verifyGoal({username: $scope.username, hash: goal.hash}).$promise
            .then(function (response) {
                goal.completed = response.status;
                $scope.gameCompleted = response.all_completed;
            });
    };
});