'use strict'

module zuehlkepage {
    
    interface IGroupFilterScope extends ng.IScope{
        toggleItem: (item: Group)  => void;
        toggleAll: ()  => void;
        groups: Group[];
        allSelected: boolean;
    }

    export function groupFilterFactory(): ng.IDirective {
        return {
			scope: {
				groups: '=',
                allSelected: '='
			},
			link:  function (scope: IGroupFilterScope) {
				new GroupFilter(scope);
			},
            templateUrl: 'components/groupFilter/groupFilter.html'
        };
    }
	
    
    class GroupFilter {
        constructor(private $scope : IGroupFilterScope) {
            $scope.allSelected = true;
           
            $scope.toggleAll = () => {
                $scope.allSelected = !$scope.allSelected;
                angular.forEach($scope.groups, (group) => {
                    group.selected = false;
                });
            }
            
            $scope.toggleItem = (item: Group) => {
                item.selected = !item.selected;
                $scope.allSelected = false;
            }
        }  
    }
}