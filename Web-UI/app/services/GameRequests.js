'use strict';

var two = false;
var five = false;
setTimeout(function () {two = true;},3000);
setTimeout(function () {five = true;},6000);

ShassaroApp.factory('GameRequests', function ($resource) {
    return $resource(ShassaroApp.api_host_url + '/game_requests');
});