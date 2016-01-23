'use strict'

module zuehlkepage {

    interface IViewSwitchScope extends ng.IScope{
        dataview : boolean;
        changeIcon: () => void;
	}
	
    export function viewSwitchFactory(): ng.IDirective {
        return {
            scope: {
			},
			controller: ['$scope', '$rootScope', function ($scope:IViewSwitchScope, $rootScope: ng.IScope) {
				new ViewSwitch($scope, $rootScope);
			}],
            templateUrl: 'components/viewSwitch/viewSwitch.html',
        };
    }

    
    class ViewSwitch {

        constructor(private $scope : IViewSwitchScope, private $rootScope: ng.IScope) {
            $scope.dataview = false;
            $scope.changeIcon = () => this.changeIcon();
        }  
        
        private changeIcon() {
            this.$scope.dataview = !this.$scope.dataview;
            this.$rootScope.$broadcast('SWITCH_VIEW_EVENT', this.$scope.dataview);
        }
    }
}