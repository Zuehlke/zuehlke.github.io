/// <reference path="../../typings/tsd.d.ts" />

'use strict';


module zuehlkepage {
    angular.module('zuehlkepage', ['ngTouch', 'ui.router', 'ui.bootstrap'])
		.controller('RepositoryCtrl',  ['$scope', 'DataService', RepositoryCtrl])
		.controller('MainCtrl', ['$scope', MainCtrl])
		.controller('NavbarCtrl', ['$scope', NavbarCtrl])
		.service('DataService', ['$http', '$q', DataService])
		.controller('PeopleCtrl', ['$scope', 'DataService',PeopleCtrl])
		.directive('viewSwitch', [viewSwitchFactory])
		.directive('jsonItemView', [jsonItemViewFactory])
		.directive('groupFilter', [groupFilterFactory])

	.config(["$stateProvider", "$urlRouterProvider", (
		$stateProvider: any,
		$urlRouterProvider: any) => {
			$stateProvider
			  .state('main', {
				url: '/main',
					templateUrl: 'app/main/main.html',
					controller: 'MainCtrl'
			  })
			  .state('main.repository', {
				url: '/repository',
				views: {
					'pagecontent' : {
						templateUrl: 'app/repository/repository.html',
						controller: 'RepositoryCtrl'
					}
				}
			  })
			  .state('main.people', {
				  url: '/people',
				  views: {
					  'pagecontent' : {
						  templateUrl: 'app/people/people.html',
						  controller: 'PeopleCtrl'
					  }
				  }
			  });

			$urlRouterProvider.otherwise('/main/repository');
		}])
		.run(['$rootScope', ($rootScope: ng.IScope) => {
			var targetOffset, currentPosition,
				body = document.getElementById('scroll-anchor'),
				animateTime = 900;

				$rootScope.$on('$stateChangeSuccess', (event: any, toState: any, toParams: any, fromState: any, fromParams: any) => {
				
				if(fromState.name !== ""){

					targetOffset = 470;
					currentPosition = 0;

					body.classList.add('in-transition');
					body.style.transform = "translate(0, -"+targetOffset+"px)";

					window.setTimeout(function () {
						body.classList.remove('in-transition');
						body.style.cssText = "";
						window.scrollTo(0, targetOffset);
					}, animateTime);
				}

			});
		}]);


}
