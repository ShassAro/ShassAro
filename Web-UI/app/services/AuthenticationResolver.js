'use strict';

ShassaroApp.service('AuthenticationResolver', function ($q, $rootScope, $location, $interval, AUTH_EVENTS, AuthenticationService) {
    var resolveUserFunc = function (deferred) {
        deferred = deferred != null ? deferred : $q.defer();

        if (AuthenticationService.isAuthenticated()) {
            deferred.resolve();
        }
        else {
            deferred.reject();
            $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated, $location.path());
            console.log('not-authenticated');
            $location.path('/');
        }

        return deferred.promise;
    };

    var firstTimeResolveFunc = function () {
        var deferred = $q.defer();

        var maxRetryCount = 10; var retryCount = 0;
        var interval = $interval(function () {
            if(retryCount++ >= maxRetryCount){
                deferred.reject();
                $interval.cancel(interval);
                $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated, $location.path());
                return;
            }
            if(AuthenticationService.isAuthenticated()){
                deferred.resolve();
                $interval.cancel(interval);
            }
        },150);

        resolveObject.resolve = resolveUserFunc;
        return deferred.promise;
    };

    var resolveObject = {
        resolve: firstTimeResolveFunc
    };

    return resolveObject;
});