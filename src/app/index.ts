/// <reference path="../../typings/tsd.d.ts" />

'use strict';


module zuehlkepage {
    angular.module('zuehlkepage', ['ngTouch', 'ui.router', 'ui.bootstrap'])
		.controller('ContributionCtrl',  ['$scope', 'DataService', ContributionCtrl])
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
			  .state('main.contributions', {
				url: '/contributions',
				views: {
					'pagecontent' : {
						templateUrl: 'app/contribution/contribution.html',
						controller: 'ContributionCtrl'
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

			$urlRouterProvider.otherwise('/main/contributions');
		}])
		.run(['$rootScope', ($rootScope: ng.IScope) => {
			var targetOffset = 580,
                currentPosition = 0,
				body = document.getElementById('scroll-anchor'),
				animateTime = 900;

				$rootScope.$on('$stateChangeSuccess', (event: any, toState: any, toParams: any, fromState: any, fromParams: any) => {
				
                if(fromState.name !== "" && document.getElementsByTagName('body')[0].className != 'sl_offcanvas-open-right'){

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
