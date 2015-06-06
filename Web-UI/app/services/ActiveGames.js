'use strict';

ShassaroApp.factory('ActiveGames', function ($resource, $q) {
    var res = $resource(ShassaroApp.api_host_url + '/active_game/:username', {},{
        verifyGoal: {method: 'GET', url: ShassaroApp.api_host_url + '/active_game/:username/goal'}
    });

    //return res;

    return {
        get: res.get,
        //get: function () {
        //    var deferred = $q.defer();
        //    var startTime = new Date().addMinutes(0);
        //    deferred.resolve(
        //        {
        //            username: "roi",
        //            start_time: startTime.toISOString(),
        //            goals: [
        //                "tahat",
        //                "another-tahat"
        //            ],
        //            duration: 1,
        //            password: "@4#19856",
        //            remote_goals_count: 1,
        //            hints: [
        //                "Try to tahat (not too much tahat)",
        //                "Keep that in mind. Tahat is the shit."
        //            ],
        //            remote_username: "assaf",
        //            vnc_port: 40125,
        //            remote_ip: "172.17.0.83",
        //            docker_manager_ip: "10.0.0.8",
        //            remote_email: "assafaloni@gmail.com"
        //        }
        //    );
        //
        //    deferred.$promise = deferred.promise;
        //    return deferred;
        //},
        verifyGoal: {method: 'GET', url: ShassaroApp.api_host_url + '/active_game/:username/goal'}
    };
});
