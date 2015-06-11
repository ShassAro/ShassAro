'use strict';

ShassaroApp.factory('Quotes', function ($http,SETTINGS) {
    //return $resource(ShassaroApp.api_host_url + '/fsng/');
    return {
        get: function () {
            return $http({method: 'GET', url: SETTINGS.apiUrl + '/fsng/'});
        }
    };
});