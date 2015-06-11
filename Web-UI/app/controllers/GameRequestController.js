'use strict';

ShassaroApp.factory('GameRequestStatuses', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/game_request_statuses/:status', {}, {});
});

ShassaroApp.factory('GameRequestSocket', function ($websocket, SETTINGS, Session) {
    var socket = $websocket(SETTINGS.wsUrl + Session.user.username + '?subscribe-broadcast');
    return {
        onMessage: socket.onMessage
    };
});


ShassaroApp.controller('GameRequestController', function ($scope, $location, $interval, $timeout, GameRequestSocket, GameRequestStatuses, Quotes) {
    $scope.username = $scope.currentUser.username;
    $scope.statusNames = ['WAITING', 'DEPLOYING', 'DONE'];

    GameRequestSocket.onMessage(function (event) {
        var requestStatus = JSON.parse(event.data)[0].fields;
        GameRequestStatuses.get({status: requestStatus.status}).$promise.then(function (status) {
            requestStatus.status = status;
            $scope.setStatus({
                status: requestStatus.status.status,
                step: $scope.getStep(requestStatus.status.status),
                percent: $scope.getPercentComplete(requestStatus.status.status),
                message: requestStatus.status.message
            });
        });
    });

    $scope.stepsInfo = [];
    $scope.setStatus = function (status) {
        $scope.currentStatus = status.status;
        $scope.currentStep = status.step;
        $scope.percentComplete = status.percent;
        $scope.currentMessage = status.message;
        $scope.stepsInfo.push(status);

        if (status.step == $scope.statusNames.length) {
            $scope.currentStep += 1;
            $timeout(function () {
                $location.path('/game');
            }, 2000);
        }
    };


    $scope.getStep = function(status){
        return $scope.statusNames.indexOf(status) + 1;
    };

    $scope.getPercentComplete = function (status) {
        var step = $scope.getStep(status);
        return Math.round(100*(step / ($scope.statusNames.length)));
    };

    $scope.refreshGameRequestStatus = function () {
        var gameRequest = GameRequests.get($scope.username);
        $scope.$apply(function () {
            var status = {
                status: gameRequest.status.status,
                step: $scope.getStep(gameRequest.status.status),
                percent: $scope.getPercentComplete(gameRequest.status.status),
                message: gameRequest.status.message
            };
            $scope.setStatus(status);
        });
    };

    $scope.getQuote = function () {
        Quotes.get().success(function (quote) {
            $scope.quote = quote;
        });
    };

    $scope.getQuote();
    $scope.quotesInterval = $interval($scope.getQuote, 10*1000);
    $scope.$on('$destroy', function() {
        $interval.cancel($scope.quotesInterval);
        delete $scope.quotesInterval;
    });
});