(function () {
  'use strict';

  angular
    .module('thinkster.routes')
    .config(config);

  config.$inject = ['$routeProvider']; //inject routeProvider as dependency

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
  //tow elements: path and options object:
    $routeProvider.when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).otherwise('/');
  }
})();