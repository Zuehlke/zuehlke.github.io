'use strict';

module zuehlkepage {
    
    export class GroupItem {
        constructor(
            public title: string,
            public url: string,
            public description: string,
            public logo: string) {
        }
    }

    export class Group {
        constructor(public name: string, public items: Array<GroupItem>, public selected?: boolean){
            this.selected = false;
        }
    }
    
    export interface IDataService extends ng.IScope {
        getJsonFileContent: (fileName : string) => ng.IPromise<Array<Group>>;
    }

    export class DataService {

        constructor (private $http: ng.IHttpService, private $q : ng.IQService) {
        }
        
        public getJsonFileContent(fileName : string) : ng.IPromise<Array<Group>>{

            var deferred = this.$q.defer();
            var groups = new Array<Group>();

            this.$http.get(fileName).success((response: Group[])  => {
                angular.forEach(response["groups"], (group : Group) => {
                    groups.push(new Group(group.name, group.items));
                    deferred.resolve(groups);
                })

            }).error((err: Error) => {
                console.log("Failed loading json file ", err);
                deferred.reject("Failed loading json file ");
            });
            
            return deferred.promise;
        }
    }
}



   
