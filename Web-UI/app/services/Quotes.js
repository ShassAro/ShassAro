'use strict';

ShassaroApp.factory('Quotes', function ($http) {
    //return $resource(ShassaroApp.api_host_url + '/fsng/');
    return {
        get: function () {
            return $http({method: 'GET', url: ShassaroApp.api_host_url + '/fsng/'});
        }
    };
});