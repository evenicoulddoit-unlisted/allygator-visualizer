import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed, async } from '@angular/core/testing';

import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { VehiclesService } from './vehicles.service';


describe('AppComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      imports: [
        AgmCoreModule.forRoot({
          apiKey: 'AIzaSyAzxNOt5wJZKNcWG9OgdnyueIDuPOFLKsw'
        }),
        HttpClientModule,
        HttpClientTestingModule,
      ],
      providers: [VehiclesService],

    }).compileComponents();
  }));
  it('should create the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));
  it(`should have as title 'app'`, async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('app');
  }));
});
