'use strict';

ShassaroApp.service('Session', function ($http, $cookies, $rootScope, Users, AUTH_EVENTS, SETTINGS) {
    // Privates
    var getToken = function () {
        var cookie = $cookies.get('auth_token');
        if(!cookie)
            return null;

        return cookie.split(':')[1];
    };
    var getUsername = function () {
        var cookie = $cookies.get('auth_token');
        if(!cookie)
            return null;

        return cookie.split(':')[0];
    };

    var setCookie = function (username, token) {
        $cookies.put('auth_token', username + ':' + token);
    };
    var unsetCookie = function(){
        $cookies.remove('auth_token');
    };

    var setTokenHeader = function (token) {
        $http.defaults.headers.common.Authorization = 'Token ' + token;
    };

    var unsetTokenHeader = function(){
        delete $http.defaults.headers.common.Authorization;
    };

    // Service
    this.tryRestore = function(){
        var token = getToken();
        if(token) {
            var username = getUsername();
            var session = this;
            $http({
                method: 'POST',
                url: SETTINGS.apiUrl + '/validate_token/',
                data: {'token': token}
            }).success(function (isValid) {
                if (isValid) {
                    setTokenHeader(token);
                    Users.get({username: username}).$promise.then(function (user) {
                        session.create({user: user, token: token});
                        $rootScope.$broadcast(AUTH_EVENTS.loginSuccess, user);
                    });
                }
            });
        }
    };


    this.create = function (loginInfo) {
        this.user = loginInfo.user;
        this.token = loginInfo.token;
        setCookie(this.user.username, this.token);
        setTokenHeader(this.token);
    };

    this.destroy = function () {
        delete this.user;
        delete this.token;
        unsetCookie();
        unsetTokenHeader();
    }
});
