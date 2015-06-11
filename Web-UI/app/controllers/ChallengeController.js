'use strict';

ShassaroApp.controller('ChallengeController', function ($scope, $location, Tags, GameRequests, SETTINGS) {
    $scope.tags = Tags.get();
    $scope.tag1 = null;
    $scope.tag2 = null;

    $scope.makeGameRequest = function () {
        function generateTagUrl(tag) {
            return SETTINGS.apiUrl + '/tags/' + tag.name + '/';
        }

        GameRequests.save({
            username: $scope.currentUser.username,
            tags: [generateTagUrl($scope.tag1), generateTagUrl($scope.tag2)]
        });
        $location.path('/gameRequest');
    }
});