import { Routes , RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import {HistoryComponent} from "./history/history.component";

const APP_ROUTES: Routes =  [
  { path: 'home', component: HomeComponent },
  { path: 'history', component: HistoryComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', redirectTo: 'home', pathMatch: 'full' },
];

export const ROUTES = RouterModule.forRoot(APP_ROUTES);
