(function () {
  'use strict';

  angular
    .module('thinkster.config')
    .config(config);

  config.$inject = ['$locationProvider'];

  /**
  * @name config
  * @desc Enable HTML5 routing
  */
  function config($locationProvider) {
    $locationProvider.html5Mode(true); //gets rid of the hash sign in the URL, ex: www.google.com/#/search
    $locationProvider.hashPrefix('!'); //turns the # into a #!. This is mostly for the benefit of search engines.
  }
})();