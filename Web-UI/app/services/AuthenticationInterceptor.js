'use strict';

ShassaroApp.factory('AuthenticationInterceptor', function ($rootScope, $q, AUTH_EVENTS) {
    return {
        responseError: function (response) {
            $rootScope.$broadcast({
                401: AUTH_EVENTS.notAuthenticated,
                403: AUTH_EVENTS.notAuthenticated
            }[response.status], response);

            return $q.reject(response);
        }
    }
});

ShassaroApp.config(function ($httpProvider) {
    $httpProvider.interceptors.push(['$injector', function ($injector) {
        return $injector.get('AuthenticationInterceptor');
    }]);
});