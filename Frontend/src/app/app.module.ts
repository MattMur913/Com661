import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RockroutesComponent } from './rockroutes.component';
import { RockrouteComponent } from './rockroute.component';
import { WebService } from './web.service';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthModule } from '@auth0/auth0-angular';
import { NavComponent } from './nav.component';
import { UpdaterouteComponent } from './updateroute.component';


var routes:any =[ {
  path: '',
  component: HomeComponent
  },
  {
  path: 'rockroute/:id',
  component: RockrouteComponent
  },{
    path: 'rockroutes/:id',
    component: RockroutesComponent
    },
    {
      path: 'updateroute/:id',
      component: UpdaterouteComponent
      }
];


@NgModule({
  declarations: [
    AppComponent,
    RockroutesComponent,
    RockrouteComponent,
    HomeComponent,
    UpdaterouteComponent,
    NavComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    AuthModule.forRoot({
      domain:'dev-h30jhc2d2p4oqr3j.us.auth0.com',
      clientId:'9aZeA2KKNJDDM2cMeXHKPuf9a2I7Jviv'
    }
    )
  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }
