'use strict';

var two = false;
var five = false;
setTimeout(function () {two = true;},3000);
setTimeout(function () {five = true;},6000);

ShassaroApp.factory('GameRequests', function ($resource, SETTINGS) {
    return $resource(SETTINGS.apiUrl + '/game_requests/');
});