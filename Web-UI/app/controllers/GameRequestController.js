'use strict';

ShassaroApp.factory('GameRequestStatuses', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/game_request_statuses/:status', {}, {});
});

ShassaroApp.factory('GameRequestSocket', function ($websocket, $interval, SETTINGS, Session) {
    return {
        getSocket: function () {
            console.log('Getting a GameRequest socket');
            var socket = $websocket(SETTINGS.wsUrl + Session.user.username + '?subscribe-broadcast&echo');
            var heartbeatMessage = '--heartbeat--', heartbeatInterval = null, missedHeartbeats = 0;

            socket.onOpen(function () {
                console.debug('gamerequestsocket on-open');
                console.debug(arguments);
                //missedHeartbeats = 0;
                //heartbeatInterval = $interval(function () {
                //    try
                //    {
                //        missedHeartbeats++;
                //        console.debug(missedHeartbeats);
                //        if(missedHeartbeats >= 10)
                //            throw new Error("Too many missed heartbeats");
                //        socket.send(heartbeatMessage);
                //    }
                //    catch(e){
                //        console.error(e);
                //        $interval.cancel(heartbeatInterval);
                //        heartbeatInterval = null;
                //        socket.close();
                //    }
                //},2000);
            });

            //socket.onMessage(function (event) {
            //    if(event.data === heartbeatMessage) {
            //        missedHeartbeats = 0;
            //        console.debug('zeroing missed heartbeats');
            //        socket.send(heartbeatMessage);
            //    }
            //});

            socket.onClose(function () {
                console.debug('gamerequestsocket on-close');
                console.debug(arguments);
                $interval.cancel(heartbeatInterval);
            });

            socket.onError(function () {
                console.debug('gamerequestsocket on-error ');
                console.debug(arguments);
            });

            return socket;
        }
    }
});


ShassaroApp.controller('GameRequestController', function ($scope, $location, $interval, $timeout, $http, GameRequests, GameRequestStatuses, Quotes) {
    $scope.username = $scope.currentUser.username;
    $scope.statusNames = ['WAITING', 'DEPLOYING', 'DONE'];
    //$scope.socket = GameRequestSocket.getSocket();
    //$scope.socket.onMessage(function (event) {
    //    var requestStatus = JSON.parse(event.data)[0].fields;
    //    GameRequestStatuses.get({status: requestStatus.status}).$promise.then(function (status) {
    //        requestStatus.status = status;
    //        $scope.setStatus({
    //            status: requestStatus.status.status,
    //            step: $scope.getStep(requestStatus.status.status),
    //            percent: $scope.getPercentComplete(requestStatus.status.status),
    //            message: requestStatus.status.message
    //        });
    //    });
    //});

    $scope.pollInterval = $interval(function () {
        GameRequests.get({username: $scope.username}).$promise.then(function (requestStatus) {
            $http.get(requestStatus.status).success(function (status) {
                requestStatus.status = status;
                $scope.setStatus({
                    status: requestStatus.status.status,
                    step: $scope.getStep(requestStatus.status.status),
                    percent: $scope.getPercentComplete(requestStatus.status.status),
                    message: requestStatus.status.message
                });
            });
        });
    }, 2000);

    $scope.stepsInfo = [];
    $scope.setStatus = function (status) {
        if(status.status == $scope.currentStatus){
            return;
        }

        $scope.currentStatus = status.status;
        $scope.gameRequestError = $scope.currentStatus == 'ERROR';
        $scope.currentStep = status.step;
        $scope.percentComplete = status.percent;
        $scope.currentMessage = status.message;
        $scope.stepsInfo.push(status);

        if ($scope.currentStatus == $scope.statusNames[2]) {
            $scope.currentStep += 1;
            $timeout(function () {
                $location.path('/game');
            }, 2000);
        }
    };

    $scope.isCurrentStep = function (stepInfo) {
        return $scope.stepsInfo.indexOf(stepInfo) == ($scope.stepsInfo.length - 1);
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
        //$scope.socket.close();
        $interval.cancel($scope.quotesInterval);
        $interval.cancel($scope.pollInterval);
    });
});