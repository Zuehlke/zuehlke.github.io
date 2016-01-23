/// <reference path="../../../typings/tsd.d.ts" />

'use strict';
/*@ngInject*/
module zuehlkepage {
/*@ngInject*/
    interface MainCtrlScope {
        showSidebar: () => void;
	}
/*@ngInject*/
    export class MainCtrl {
		/* @ngInject */
        constructor(private $scope: any){

			$scope.showSidebar = () => {
                var bodyClassName = document.getElementsByTagName('body')[0].className;
                
                if(bodyClassName.indexOf('sl_offcanvas-open-right') !== -1){
                    document.getElementsByTagName('body')[0].className = '';
                }else{
                    document.getElementsByTagName('body')[0].className += 'sl_offcanvas-open-right';
                }
            };
        }  
    }
}