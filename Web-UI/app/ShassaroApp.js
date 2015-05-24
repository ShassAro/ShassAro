var ShassaroApp = angular.module('ShassaroApp', ['ngRoute','ngResource','noVNC','ui.bootstrap','timer','ngWebSocket']);

ShassaroApp.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $routeProvider.

        when('/challenge', {
            templateUrl: 'views/Challenge.html',
            controller: 'ChallengeController'
        }).
        when('/gameRequest', {
            templateUrl: 'views/GameRequest.html',
            controller: 'GameRequestController'
        }).
        when('/game',{
            templateUrl: 'views/Game.html',
            controller: 'GameController'
        }).
        when('/login',{
            templateUrl: 'views/Login.html'

        }).
        when('/aboutUs',{
            templateUrl: 'views/AboutUs.html'

        }).
        when('/aboutShassaro',{
            templateUrl: 'views/aboutShassaro.html'

        }).
        otherwise('/challenge');
}]);


//ShassaroApp.username = "shay";
ShassaroApp.api_host_url = 'http://192.168.2.111:1234';