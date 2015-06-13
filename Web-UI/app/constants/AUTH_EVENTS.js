'use strict';

ShassaroApp.constant('AUTH_EVENTS',{
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized'
});

ShassaroApp.constant('SETTINGS',{
    //apiUrl: 'http://10.0.0.9:1234',
    apiUrl: 'http://www.shassaro.com/api/bl',
    //wsUrl: 'ws://10.0.0.9:1234/ws/'
    wsUrl: 'ws://www.shassaro.com/ws/'
});