function resolveAuthenticatedUser($q, $timeout, $interval){
    var deferred = $q.defer();
    function resolveWhenShassaroUserDefined(){
        if(angular.isDefined(ShassaroApp.user))
            deferred.resolve(ShassaroApp.user);
    }

    resolveWhenShassaroUserDefined();
    var interval = $interval(resolveWhenShassaroUserDefined, 500);

    $timeout(function () {
        deferred.reject(ShassaroApp.user);
        $interval.cancel(interval);
    }, 3000);

    return deferred.promise;
}

var ShassaroApp = angular
    .module('ShassaroApp', ['ngRoute','ngResource','noVNC','ui.bootstrap','timer','ngWebSocket', 'ui.gravatar', 'ngCookies', 'timer'])
    .config(['$routeProvider', '$locationProvider', function ($routeProvider) {
        $routeProvider.
            when('/challenge', {
                templateUrl: 'views/Challenge.html',
                controller: 'ChallengeController'
            }).
            when('/gameRequest', {
                templateUrl: 'views/GameRequest.html',
                controller: 'GameRequestController',
                resolve: { user: function ($q, $timeout, $interval) { return resolveAuthenticatedUser($q, $timeout, $interval); } }
            }).
            when('/game', {
                templateUrl: 'views/Game.html',
                controller: 'GameController',
                resolve: { user: function ($q, $timeout, $interval) { return resolveAuthenticatedUser($q, $timeout, $interval); } }
            }).
            when('/login', {
                templateUrl: 'views/Login.html'

            }).
            when('/aboutUs', {
                templateUrl: 'views/AboutUs.html'

            }).
            when('/aboutShassaro', {
                templateUrl: 'views/aboutShassaro.html'

            }).
            when('/dashboard', {
                templateUrl: 'views/DashboardView.html'
            }).
            when('/gameResult', {
                templateUrl: 'views/GameResult.html'
            }).
            when('/', {
                templateUrl: 'views/main.html'
            }).

            otherwise('/challenge');
    }]);

ShassaroApp.api_host_url = 'http://10.0.0.8:1234';
//ShassaroApp.api_host_url = 'http://www.shassaro.com/api/bl';