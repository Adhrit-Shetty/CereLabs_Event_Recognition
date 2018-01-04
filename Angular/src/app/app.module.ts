import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { VideoboxComponent } from './home/videobox/videobox.component';
import { ControlpanelComponent } from './home/controlpanel/controlpanel.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import {ReactiveFormsModule} from "@angular/forms";
import { AddKnownComponent } from './add-known/add-known.component';

import { HistoryComponent } from './history/history.component';
import {LoginService} from "./shared/login.service";
import { ROUTES } from './app.routing';
import { RouterModule } from '@angular/router'

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    VideoboxComponent,
    ControlpanelComponent,
    HomeComponent,
    LoginComponent,
    AddKnownComponent,
    HistoryComponent
  ],
  imports: [
    BrowserModule,
    RouterModule,
    ROUTES,
    ReactiveFormsModule
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule { }
