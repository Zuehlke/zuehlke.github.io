'use strict';

module zuehlkepage {
    interface IRepositoryScope extends ng.IScope {
        groups: Array<Group>;
    }

    export class RepositoryCtrl {
    /* @ngInject */
        constructor ($scope: IRepositoryScope, DataService: IDataService) {
            DataService.getJsonFileContent("./files/repositories.json").then((groups: Array<Group>) => {
                $scope.groups = groups;
            });
        }
    }
}

