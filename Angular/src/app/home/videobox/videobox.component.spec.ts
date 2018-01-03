import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoboxComponent } from './videobox.component';

describe('VideoboxComponent', () => {
  let component: VideoboxComponent;
  let fixture: ComponentFixture<VideoboxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VideoboxComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VideoboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
