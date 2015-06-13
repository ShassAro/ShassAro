'use strict';

ShassaroApp.factory('ActiveGames', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/active_game/:username', {}, {
        verifyGoal: {method: 'GET', url: SETTINGS.apiUrl + '/active_game/:username/goal'},
        giveUp: {method: 'POST', url: SETTINGS.apiUrl + '/forfeit/'}
    });
});
