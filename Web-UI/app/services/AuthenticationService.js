'use strict';

ShassaroApp.factory('Users', function ($resource, $q) {
    var resource = $resource(ShassaroApp.api_host_url + '/users/:username');
    return resource;

    //return {
    //    get: resource.get
    //    //get: function () {
    //    //    var deferred = $q.defer();
    //    //    deferred.resolve({
    //    //        username: "assaf",
    //    //        email: "assafaloni@gmail.com",
    //    //        first_name: "Assaf",
    //    //        last_name: "Aloni"
    //    //    });
    //    //
    //    //    deferred.$promise = deferred.promise;
    //    //
    //    //    return deferred;
    //    //}
    //};
});

ShassaroApp.constant('AUTH_EVENTS',{
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized'
});

ShassaroApp.service('Session', function ($http, $cookies, $rootScope, Users, AUTH_EVENTS) {
    // Init session
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

    this.tryRestore = function(){
        var token = getToken();
        if(token) {
            var username = getUsername();
            var session = this;
            $http({
                method: 'POST',
                url: ShassaroApp.api_host_url + '/validate_token/',
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

ShassaroApp.factory('AuthenticationService', function ($http, $q, Session) {
    var authService = {};

    authService.login = function (credentials) {
        var authHeader = btoa(credentials.username + ':' + credentials.password);
        return $http(
            {
                method: 'POST',
                url: ShassaroApp.api_host_url + '/login/',
                headers: {
                    "Authorization": "Basic " + authHeader
                }
            })
            .success(function (response) {
                Session.create({user: response.user, token: response.token});
            });
    };

    authService.logout = function () {
        return $http(
            {
                method: 'DELETE',
                url: ShassaroApp.api_host_url + '/logout/'
            })
            .success(function () {
                Session.destroy()
            });
    };

    authService.validateToken = function (token) {
        var deferred = $q;
        $http({
            method: 'POST',
            url: ShassaroApp.api_host_url + '/validate_token/',
            data: {'token': token}
        }).success(function (isValid) {
            if(isValid){
                deferred.resolve();
            }
            else{
                deferred.reject();
            }
        });
        return deferred.promise;
    };

    authService.isAuthenticated = function () {
        return !!Session.user;
    };

    return authService;
});

ShassaroApp.service('AuthenticationResolver', function ($q, $rootScope, AUTH_EVENTS) {
    var resolveUser = $q.defer();
    $rootScope.$on(AUTH_EVENTS.loginSuccess, function (event, data){
        resolveUser.resolve();
    });

    return {
        resolve: function () {
            return resolveUser.promise;
            //
            //var deferred = $q.defer();
            //
            //return deferred.promise;
            //
            //var unwatch = $rootScope.$watch('currentUser', function (currentUser) {
            //    if(angular.isDefined(currentUser)){
            //        if(currentUser){
            //            deferred.resolve(currentUser);
            //            //unwatch();
            //        }
            //        else{
            //            deferred.reject();
            //            console.error('show user login dialog');
            //        }
            //    }
            //});
            //
            //return deferred.promise;
        }
    }
});

ShassaroApp.factory('AuthenticationService_OLD', function ($http, $cookies, $q, Users) {

    var isAuthenticated = false;
    var username = null;

    function validateToken(token) {
        return $http({
            method: 'POST',
            url: ShassaroApp.api_host_url + '/validate_token/',
            data: {'token': token}
        });
    }

    var auth = {
        userDataResolved: $q.defer(),
        isAuthenticated: function () {
            var deferred = $q.defer();
            var result = {
                true: deferred.promise.then,
                false: deferred.promise.catch
            };

            var token = auth.getToken();
            if(token == null){
                deferred.reject();
            }
            else {
                validateToken(token)
                    .success(function (tokenIsValid) {
                        if (tokenIsValid) {
                            deferred.resolve();
                        }
                        else {
                            deferred.reject();
                        }
                    });
            }
            return result;
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

    function setAuthenticationDetails(token){
        if(!angular.isDefined(token))
            var token = auth.getToken();

        auth.setTokenHeader(token);
        auth.setAuthenticatedUserInfo();
    }

    if(auth.isAuthenticated()){
        setAuthenticationDetails();
    }

    var self = this;
    return {
        userDataResolved: function () {
            return auth.userDataResolved.promise;
        },
        getUsername: function () { return auth.getUsername(); },
        isAuthenticated: auth.isAuthenticated,
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
                    self.username = username;
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