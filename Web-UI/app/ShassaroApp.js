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

var resolveUser = {
    user: function resolveAuthentication(AuthenticationResolver) {
        return AuthenticationResolver.resolve();
    }
};
var ShassaroApp = angular
    .module('ShassaroApp', ['ngRoute','ngResource','noVNC','ui.bootstrap','timer','ngWebSocket', 'ui.gravatar', 'ngCookies', 'timer'])
    .config(['$routeProvider', '$locationProvider', function ($routeProvider) {
        $routeProvider.
            when('/challenge', {
                templateUrl: 'views/Challenge.html',
                controller: 'ChallengeController',
                resolve: resolveUser
            }).
            when('/gameRequest', {
                templateUrl: 'views/GameRequest.html',
                controller: 'GameRequestController',
                resolve: resolveUser
                //resolve: { user: function ($q, $timeout, $interval) { return resolveAuthenticatedUser($q, $timeout, $interval); } }
            }).
            when('/game', {
                templateUrl: 'views/Game.html',
                controller: 'GameController',
                resolve: resolveUser
                //resolve: { user: function ($q, $timeout, $interval) { return resolveAuthenticatedUser($q, $timeout, $interval); } }
            }).
            when('/gameResult',{
                templateUrl: 'views/GameResult.html',
                controller: 'GameResultController',
                resolve: resolveUser
            }).
            when('/login', {
                templateUrl: 'views/Login.html'

            }).
            when('/aboutUs', {
                templateUrl: 'views/AboutUs.html'

            }).
            when('/aboutShassaro', {
                templateUrl: 'views/AboutShassaro.html'

            }).
            when('/dashboard', {
                templateUrl: 'views/DashboardView.html'
            }).
            when('/', {
                templateUrl: 'views/Main.html'
            }).
            otherwise('/');
    }]);

ShassaroApp.config(function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
});