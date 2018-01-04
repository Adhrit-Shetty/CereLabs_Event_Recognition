export class LoginService{
  x:boolean = true;

  setLoggedIn() {
    this.x = true;
    return true;
  }
  setLoggedOut() {
    this.x = false;
    return false;
  }
  getStatus(){
    return this.x;
  }
}
