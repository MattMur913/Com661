import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class WebService {
  area_list: any;
  private routeID:any;
  private areaID:any;
  urled:any;


  constructor(private http: HttpClient) {}
  //gets all areas
  getClimbs(page:number) {return this.http.get('http://localhost:5000/api/v1.0/areas?pn='+page);}
  //returns a singular area
  getClimb(id:any) {
    this.areaID = id;
    return this.http.get('http://localhost:5000/api/v1.0/areas/'+id);
  }
  //gets all routes for an area
  getRoutes(id:any) {
    this.areaID=id
    return this.http.get('http://localhost:5000/api/v1.0/areas/'+this.areaID +'/routes');}

  //gets a singluar route from an area
  getRoute(rid:any, id:any) {
    this.areaID=id
    this.routeID = rid;
    return this.http.get('http://localhost:5000/api/v1.0/areas/'+id +'/routes/'+rid);
  }

  //displays comments for an area
  getComments(rid:any, id:any) {
    this.areaID=id
    this.routeID = rid;
    return this.http.get('http://localhost:5000/api/v1.0/comments/'+id +'/routes/'+rid);
  }

  //deletes a route
  deleteRoute(rid:any,id:any){
    return this.http.delete('http://localhost:5000/api/v1.0/deleteroute/'+id+'/routes/'+rid);
  }

  //deletes a comment
  deleteComment(rid:any,id:any,cid:any){
    return this.http.delete('http://localhost:5000/api/v1.0/deletecomment/'+id+'/routes/'+rid+'/cid/'+cid);
  }

  //updates a route
  updateRoute(updates:any,rid:any,aid:any){

    //checker
    console.log(this.areaID + this.routeID)
    console.log(aid + rid)

    //creates the form data
    let postData = new FormData();
    postData.append("Route",updates.route);
    postData.append("RouteType",updates.routeType);
    postData.append("Grade",updates.Grade);
    postData.append("Pitches",updates.pitches);
    postData.append("Length",updates.length);
    this.urled = this.http.put('http://localhost:5000/api/v1.0/areas/'+ aid +'/routes/' +rid, postData);
    return this.urled;
  }


  //adds a commemnt
  postComment(comment:any){
    //creates the form data
    let postData= new FormData();
    postData.append("username",comment.username);
    postData.append("comment",comment.comment);
    postData.append("rating",comment.rating);
    let today = new Date();
    let todayDate = today.getFullYear + "-" + today.getMonth + "-"+today.getDay;
    postData.append("date",todayDate);
    //sends the form
    return this.http.post('http://localhost:5000/api/v1.0/addComment/'+this.areaID +'/routes/' +this.routeID, postData);
  }


}


