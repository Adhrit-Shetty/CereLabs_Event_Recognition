import { Component } from '@angular/core';
import { LoginService } from './shared/login.service'
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private login: LoginService){}
  title = 'app';

  checkLogin(){
    return this.login.getStatus() === true;
  }
}
