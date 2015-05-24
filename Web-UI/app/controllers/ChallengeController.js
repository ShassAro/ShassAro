'use strict';

ShassaroApp.controller('ChallengeController', function ($scope, $location, Tags, GameRequests) {
    $scope.tags = Tags.get();
    $scope.tag1 = null;
    $scope.tag2 = null;

    $scope.makeGameRequest = function () {
        var response = GameRequests.save({
            tags: [{
                name: $scope.tag1,
                description: ''
            }, {
                name: $scope.tag2,
                description: ''
            }]
        });

        $location.path('/gameRequest');
    }
});