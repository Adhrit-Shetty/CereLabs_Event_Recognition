import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddKnownComponent } from './add-known.component';

describe('AddKnownComponent', () => {
  let component: AddKnownComponent;
  let fixture: ComponentFixture<AddKnownComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddKnownComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddKnownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
