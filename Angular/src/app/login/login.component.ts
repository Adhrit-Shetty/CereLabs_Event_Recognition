import { Component, OnInit } from '@angular/core';
import {FormArray, FormControl, FormGroup, Validators} from "@angular/forms";
import {Observable} from "rxjs/Observable";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  genders = ['male', 'female'];
  signupForm: FormGroup;

  ngOnInit() {
    this.signupForm = new FormGroup({
      'userData': new FormGroup({
        'username': new FormControl(null, [Validators.required, this.lengthCheck.bind(this)]),
        'pass': new FormControl(null, [Validators.required, this.lengthCheck.bind(this), this.characterCheck.bind(this)]),
      }),
    });
  }

  onSubmit() {
    console.log(this.signupForm.status);
    if(this.signupForm.status === 'VALID'){
      console.log('do something!');
    }
    // this.signupForm.reset();
  }

  lengthCheck(control: FormControl): { [s: string]: boolean } {
    console.log('here');
    if(control.value !== null && control.value.length>=3)
    {
      return null;
    }
    return  {'badLength': true};
  }

  characterCheck(control: FormControl): { [s: string]: boolean } {
    var pattern1 = /.*[0-9].*/;
    var pattern2 = /.*[A-Z].*/;
    var name = control.value;
    if(pattern1.test(name) === true && pattern2.test(name) === true){
      return null;
    }
    return  {'badCharacter': true};
  }
}
