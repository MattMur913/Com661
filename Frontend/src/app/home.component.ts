import { Component } from '@angular/core';
import { WebService } from './web.service';


@Component({
 selector: 'home',
 templateUrl: './home.component.html',
 styleUrls: ['./home.component.css']
})
export class HomeComponent {
  area_list: any = [];
  page: number=1;

  constructor(public webService: WebService) {};

  ngOnInit() {
    if(sessionStorage['page']){
      this.page=Number(sessionStorage['page'])
    }

    this.area_list = this.webService.getClimbs(this.page);
    }

  previousPage() {
    if (this.page > 1) {
      this.page = this.page - 1;
      sessionStorage['page'] = this.page
      this.area_list = this.webService.getClimbs(this.page);
      }
  }
  nextPage() {
    this.page = this.page + 1;
    sessionStorage['page'] =this.page
    this.area_list = this.webService.getClimbs(this.page);
  }


}

