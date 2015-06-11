'use strict';

ShassaroApp.factory('GameResults', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/game_results/:id');
});