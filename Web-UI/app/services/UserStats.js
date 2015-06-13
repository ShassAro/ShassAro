'use strict';

ShassaroApp.factory('UserStats', function ($resource) {
    return $resource(SETTINGS.apiUrl + '/users/:username/stats');
});