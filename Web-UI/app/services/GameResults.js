'use strict';

ShassaroApp.factory('GameResults', function ($resource, $http, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/game_results/:id', {}, {
        specificUserWinnings: {method: 'get', isArray:true, url: SETTINGS.apiUrl + '/game_results_won/:username'},
        specificUserLosings: {method: 'get', isArray:true, url: SETTINGS.apiUrl + '/game_results_lost/:username'}
    });
});