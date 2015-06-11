'use strict';

ShassaroApp.factory('Tags', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/tags', {}, {
        get: {isArray: true}
    });
});