'use strict';
ShassaroApp.factory('LoginService', function ($http) {
    return {
        login: function (username, password) {
            var authString = btoa(username + ':' + password);
            return $http({
                method: 'GET',
                url: ShassaroApp.api_host_url + '/',
                headers: {
                    "Authorization": "Basic " + authString
                }
            }).
                success(function () {
                    $http.defaults.headers.common.Authorization = authString;
                    ShassaroApp.username = username;
                });
        }
    };
});