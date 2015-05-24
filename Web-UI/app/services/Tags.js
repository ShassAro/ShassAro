'use strict';

ShassaroApp.factory('Tags', function ($resource) {
    return $resource(ShassaroApp.api_host_url + '/tags', {}, {
        get: {isArray: true}
    });
});