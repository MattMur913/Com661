import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'updateroute',
  templateUrl: './updateroute.component.html',
  styleUrls: ['./updateroute.component.css']
})
export class UpdaterouteComponent {
  routeForm:any;
  constructor(private webService: WebService,
    private route:ActivatedRoute,
    private router:Router,
    public authService:AuthService,
    private formBuilder: FormBuilder) {};


    ngOnInit() {
      this.routeForm = this.formBuilder.group({
        route:['', Validators.required],
        routeType:['', Validators.required],
        pitches:[''],
        length:[''],
        Grade:['',Validators.required]
      });

      console.log(sessionStorage['area']);
      console.log(this.route.snapshot.params['id']);      }

    isInvalid(control: any) {
      return this.routeForm.controls[control].invalid &&
      this.routeForm.controls[control].touched;
      }
    isUntouched() {
      return this.routeForm.controls.route.pristine ||
      this.routeForm.controls.Grade.pristine ||
      this.routeForm.controls.routeType.pristine ;
    }
    isIncomplete() {
      return this.isInvalid('Grade') ||
      this.isInvalid('routeType') ||
      this.isInvalid('route') ||
      this.isUntouched();
    }

    onSubmit(){
      this.webService.updateRoute(this.routeForm.value,this.route.snapshot.params['id'],sessionStorage['area']).subscribe((response:any)=>{
        this.routeForm.reset();
        this.webService.getRoute(this.route.snapshot.params['id'],sessionStorage['area']);
      });
      this.router.navigate(['/rockroute',this.route.snapshot.params['id']]);
    }


}
