'use strict';

module zuehlkepage {
    interface IContributionScope extends ng.IScope {
        groups: Array<Group>;
        allSelected: boolean;
    }

    export class ContributionCtrl {
    /* @ngInject */
        constructor ($scope: IContributionScope, DataService: IDataService) {
            $scope.allSelected = true;
            
            DataService.getJsonFileContent("./files/contributions.json").then((groups: Array<Group>) => {
                $scope.groups = groups;
            });
        }
    }
}

