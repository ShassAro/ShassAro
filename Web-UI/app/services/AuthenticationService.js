'use strict';

ShassaroApp.factory('Users', function ($resource) {
    return $resource(ShassaroApp.api_host_url + '/users/:username');
});

ShassaroApp.factory('AuthenticationService', function ($http, $cookies, $q, Users) {
    var auth = {
        userDataResolved: $q.defer(),
        isAuthenticated: function () {
            return this.getToken() != null;
        },
        getToken: function () {
            var cookie = $cookies.get('auth_token');
            if(!cookie)
                return null;

            return cookie.split(':')[1];
        },
        getUsername: function () {
            var cookie = $cookies.get('auth_token');
            if(!cookie)
                return null;

            return cookie.split(':')[0];
        },
        setCookie: function (username, token) {
            return $cookies.put('auth_token', username + ':' + token);
        },
        logoutUser : function () {
            $cookies.remove('auth_token');
            delete $http.defaults.headers.common.Authorization;
            delete ShassaroApp.user;
        },
        setTokenHeader: function (token) {
            $http.defaults.headers.common.Authorization = 'Token ' + token;
        },
        setAuthenticatedUserInfo: function (username) {
            if(username == null)
                username = this.getUsername();

            Users.get({username: username}).$promise.then(function (user) {ShassaroApp.user = user;});
            this.userDataResolved.resolve();
        }
    };

    if(auth.isAuthenticated()){
        var token = auth.getToken();
        auth.setTokenHeader(token);
        auth.setAuthenticatedUserInfo();
    }


    return {
        userDataResolved: function () {
            return auth.userDataResolved.promise;
        },
        auth : auth,
        login: function (username, password) {
            var authString = btoa(username + ':' + password);
            return $http({
                    method: 'POST',
                    url: ShassaroApp.api_host_url + '/login/',
                    headers: {
                        "Authorization": "Basic " + authString
                    }
                })
                .success(function (token) {
                    auth.setCookie(username, token);
                    auth.setTokenHeader(token);
                    auth.setAuthenticatedUserInfo(username);
                });
        },
        logout : function () {
            return $http({
                    method: 'DELETE',
                    url: ShassaroApp.api_host_url + '/logout/'
                })
                .success(function () {
                    auth.logoutUser();
                });
        },
        register: function (username, password, first_name, last_name, email) {
            return $http(                {
                    method: 'POST',
                    url: ShassaroApp.api_host_url + '/register/',
                    data: {
                        username: username,
                        password: password,
                        first_name: first_name,
                        last_name: last_name,
                        email: email
                    }
                });
        }
    };
});