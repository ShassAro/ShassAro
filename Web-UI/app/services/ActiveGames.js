'use strict';

ShassaroApp.factory('ActiveGames', function ($resource) {
    var api_host_url = 'http://10.0.0.7:1234';
    var res = $resource(api_host_url + '/active_game/:username', {},{
        verifyGoal: {method: 'GET', url: api_host_url + '/active_game/:username/goal'}
    });

    return res;

    return {
        get: res.get,
        verifyGoal: {method: 'GET', url: api_host_url + '/active_game/:username/goal'}
    };
});
