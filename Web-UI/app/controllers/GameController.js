'use strict';

ShassaroApp.controller('GameController', function ($scope, $websocket, ActiveGames) {
    var socket = $websocket(ShassaroApp.api_host_url.replace('http://','ws://')+'/ws/'+$scope.username+'-game?subscribe-broadcast');
    socket.onMessage(function (event) {
        var gameInfo = JSON.parse(event.data);
        console.log(gameInfo);
    });

    App.sidebar('close-sidebar');

    $scope.isConnected = false;
    $scope.username = ShassaroApp.user.name;
    $scope.gameCompleted = false;

    ActiveGames.get({username: $scope.username}).$promise
        .then(function (gameInfo) {
            $scope.vncHost = gameInfo.docker_manager_ip;
            $scope.vncPort = gameInfo.vnc_port;
            $scope.vncPassword = gameInfo.password;
            $scope.goals = [];
            for (var i = 0; i < gameInfo.goals.length; i++) {
                $scope.goals.push({description: gameInfo.goals[i], hint: gameInfo.hints[i]});
            }
            $scope.opponentIP = gameInfo.remote_ip;
            $scope.isConnected = true;
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