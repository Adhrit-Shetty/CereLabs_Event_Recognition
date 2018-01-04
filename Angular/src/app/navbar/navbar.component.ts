import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  tab: string = 'home';

  changeTab(data:string){
    this.tab = data;
    console.log(this.tab);
  }

  constructor() { }

  ngOnInit() {
  }

}
