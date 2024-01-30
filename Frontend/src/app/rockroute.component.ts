import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'rockroute',
  templateUrl: './rockroute.component.html',
  styleUrls: ['./rockroute.component.css']
})
export class RockrouteComponent{
  area_list: any=[];
  routes_list: any=[];
  comment_list: any=[];
  routeID:any;

  commentForm: any;

  constructor(private webService: WebService,
    private route:ActivatedRoute,
    private router:Router,
    public authService:AuthService,
    private formBuilder: FormBuilder) {};

  ngOnInit() {

    this.commentForm = this.formBuilder.group({
      username:['', Validators.required],
      comment:['',Validators.required],
      rating:5
    });

      this.routes_list =this.webService.getRoute(this.route.snapshot.params['id'],sessionStorage['area']);
      this.comment_list =this.webService.getComments(this.route.snapshot.params['id'],sessionStorage['area']);
      this.routeID = this.route.snapshot.params['id'];
    }



  onSubmit(){
    this.webService.postComment(this.commentForm.value).subscribe((response:any)=>{
      this.commentForm.reset();
      this.routes_list =this.webService.getRoute(this.route.snapshot.params['id'],sessionStorage['area']);
    });
    this.commentForm.reset();
  }

  deleteClimb(){
    this.webService.deleteRoute(this.route.snapshot.params['id'], sessionStorage['area']).subscribe(() => {
      this.router.navigate(['/']);
    });
  }

  deleteComment(commentID:any){
    this.webService.deleteComment(this.route.snapshot.params['id'], sessionStorage['area'],commentID).subscribe(() => {
      this.router.navigate(['/']);
    });
  }

  }
