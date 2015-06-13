'use strict';

ShassaroApp.factory('Users', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/users/:username');
});
