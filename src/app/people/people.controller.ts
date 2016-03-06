'use strict';

module zuehlkepage {

  interface IPeopleScope extends ng.IScope {
      groups: Array<Group>; 
      allSelected:  boolean;
  }
  export class PeopleCtrl {
    /* @ngInject */
    constructor (private $scope: IPeopleScope, DataService: IDataService) {
        $scope.allSelected =  true;
        
        DataService.getJsonFileContent("./files/people.json").then((groups: Array<Group>) => {
            $scope.groups = groups;
        });
    }
  }
}



