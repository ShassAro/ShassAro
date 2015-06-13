var ShassaroApp = angular
    .module('ShassaroApp', ['ngRoute','ngResource','noVNC','ui.bootstrap','timer','ngWebSocket', 'ui.gravatar', 'ngCookies', 'timer'])
    .config(['$routeProvider', '$locationProvider', function ($routeProvider) {

        var routeResolveUser = {
            user: function resolveAuthentication(AuthenticationResolver) {
                return AuthenticationResolver.resolve();
            }
        };

        $routeProvider.
            when('/challenge', {
                templateUrl: 'views/Challenge.html',
                controller: 'ChallengeController',
                resolve: routeResolveUser
            }).
            when('/gameRequest', {
                templateUrl: 'views/GameRequest.html',
                controller: 'GameRequestController',
                resolve: routeResolveUser
            }).
            when('/game', {
                templateUrl: 'views/Game.html',
                controller: 'GameController',
                resolve: routeResolveUser
            }).
            when('/gameResult',{
                templateUrl: 'views/GameResult.html',
                controller: 'GameResultController',
                resolve: routeResolveUser
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
                templateUrl: 'views/DashboardView.html',
                controller: 'DashboardController',
                resolve: routeResolveUser
            }).
            when('/', {
                templateUrl: 'views/Main.html'
            }).
            otherwise('/');
    }])
    .config(function($resourceProvider) {
        // for comparability with django rest framework - make sure trailing slashes exist
        $resourceProvider.defaults.stripTrailingSlashes = false;
    })
    .run(function ($rootScope, AUTH_EVENTS, AuthenticationService) {
        // When a route changes - raise 'AUTH_EVENTS.notAuthenticated' if the user is not authenticated
        //$rootScope.$on('$routeChangeStart', function (event, next) {
        //    if(!AuthenticationService.isAuthenticated()){
        //        event.preventDefault();
        //        $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
        //    }
        //});
    });