'use strict'

module zuehlkepage {
    
    interface IGroupFilterScope extends ng.IScope{
        toggleItem: (item: Group)  => void;
        toggleAll: ()  => void;
        groups: Group[];
        selectAll: boolean;
    }

    export function groupFilterFactory(): ng.IDirective {
        return {
			scope: {
				groups: '='  
			},
			link:  function (scope: IGroupFilterScope) {
							new GroupFilter(scope);
			},
            templateUrl: 'components/groupFilter/groupFilter.html'
        };
    }
	
    
    class GroupFilter {
        constructor(private $scope : IGroupFilterScope) {
            $scope.selectAll = true;
            
            $scope.toggleAll = () => {
                $scope.selectAll = !$scope.selectAll;
               
                angular.forEach($scope.groups, (group) => {
                    if($scope.selectAll){
                        group.selected =  true;
                    }else {
                        group.selected = false; 
                    }
                });
            }
            
            $scope.toggleItem = (item: Group) => {
                item.selected = !item.selected;
            }
        }  
    }
}