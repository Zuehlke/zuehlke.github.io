'use strict'


module zuehlkepage {
    
    interface IJsonItemViewScope extends ng.IScope{
        groups: Group[];
        showList: boolean;
        fileName: string;
        flatList: Array<any>;
        isGroupSelected:(string) => boolean;
        allSelected: boolean;
    }
    
    export function jsonItemViewFactory(): ng.IDirective {
        return {
			scope : {
				groups: '=',
                allSelected: '='
			},
			controller: ['$scope', function ($scope:IJsonItemViewScope) {
                new JsonItemView($scope);
			}],
           
            templateUrl: 'components/jsonItemView/jsonItemView.html'
        };
    }
	
	jsonItemViewFactory.$inject = ['$scope'];
    
    class JsonItemView {
        constructor(private $scope : IJsonItemViewScope) {
            $scope.showList = false;
            $scope.flatList = [];
            
            $scope.$on('SWITCH_VIEW_EVENT', (event, showList) => {
                $scope.showList = showList;
            });
            
            angular.forEach($scope.groups, (group: Group) => {
                angular.forEach(group.items, (item: GroupItem) => {
                    $scope.flatList.push({"groupname" : group.name, "item" : item});
                });
            });
            
            this.$scope.isGroupSelected = (groupname: string) => this.isGroupSelected(groupname);
        } 
        
        private isGroupSelected(name: string) : boolean {
            if(!name) return true;
            var found = false;
    
            angular.forEach(this.$scope.groups, (group: Group) => {
                if((group.name === name) && group.selected){
                    found = true;
                }
            }); 
            return found;
        }
    }
}