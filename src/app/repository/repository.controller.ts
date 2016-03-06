'use strict';

module zuehlkepage {
    interface IRepositoryScope extends ng.IScope {
        groups: Array<Group>;
        allSelected: boolean;
    }

    export class RepositoryCtrl {
    /* @ngInject */
        constructor ($scope: IRepositoryScope, DataService: IDataService) {
            $scope.allSelected = true;
            
            DataService.getJsonFileContent("./files/repositories.json").then((groups: Array<Group>) => {
                $scope.groups = groups;
            });
        }
    }
}

