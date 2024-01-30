import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'rockroutes',
  templateUrl: './rockroutes.component.html',
  styleUrls: ['./rockroutes.component.css']
})
export class RockroutesComponent{
  route_list: any = [];
  area_list:any = [];
  page: number=1;

  constructor(private route:ActivatedRoute, public webService: WebService) {};

  ngOnInit() {
    if(sessionStorage['page']){
      this.page=Number(sessionStorage['page'])
    }

    sessionStorage['area']=this.route.snapshot.params['id'];
    this.area_list = this.webService.getClimb(sessionStorage['area']);
    console.log(this.area_list)
    this.route_list = this.webService.getRoutes(this.route.snapshot.params['id']);
    }


}
