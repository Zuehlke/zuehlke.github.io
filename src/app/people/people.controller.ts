'use strict';

module zuehlkepage {
    
  interface IPeopleScope extends ng.IScope {
      groups: Array<Group>;
  }
  export class PeopleCtrl {
    /* @ngInject */
    constructor (private $scope: IPeopleScope, DataService: IDataService) {
        DataService.getJsonFileContent("./files/people.json").then((groups: Array<Group>) => {
            $scope.groups = groups;
        });
    }
  }
}



