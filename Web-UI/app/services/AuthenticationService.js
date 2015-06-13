'use strict';

ShassaroApp.factory('AuthenticationService', function ($http, $q, $rootScope, Session, AUTH_EVENTS, SETTINGS) {
    var authService = {};

    authService.register = function (registration) {
        return $http(                {
            method: 'POST',
            url: SETTINGS.apiUrl + '/register/',
            data: {
                username: registration.username,
                password: registration.password,
                first_name: registration.first_name,
                last_name: registration.last_name,
                email: registration.email
            }
        });
    };

    authService.login = function (credentials) {
        var authHeader = btoa(credentials.username + ':' + credentials.password);
        return $http(
            {
                method: 'POST',
                url: SETTINGS.apiUrl + '/login/',
                headers: {
                    "Authorization": "Basic " + authHeader
                }
            })
            .success(function (response) {
                Session.create({user: response.user, token: response.token});
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess, response.user);
            });
    };

    authService.logout = function () {
        return $http(
            {
                method: 'DELETE',
                url: SETTINGS.apiUrl + '/logout/'
            })
            .success(function () {
                Session.destroy();
                $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
            });
    };

    authService.validateToken = function (token) {
        var deferred = $q;
        $http({
            method: 'POST',
            url: SETTINGS.apiUrl + '/validate_token/',
            data: {'token': token}
        }).success(function (isValid) {
            if(isValid){
                deferred.resolve();
            }
            else{
                deferred.reject();
            }
        }).error(function () {
            deferred.reject();
        });

        return deferred.promise;
    };

    authService.isAuthenticated = function () {
        return !!Session.user;
    };

    return authService;
});