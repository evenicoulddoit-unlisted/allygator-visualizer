import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed, inject } from '@angular/core/testing';

import { VehiclesService } from './vehicles.service';


const HttpClientMock = jasmine.createSpyObj('HttpClient', ['get']);


describe('VehiclesService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule
      ],
      providers: [VehiclesService]
    });
  });

  it('should be created', inject(
    [VehiclesService, HttpTestingController],
    (service: VehiclesService, backend: HttpTestingController) => {
      expect(service).toBeTruthy();
    }
  ));
});
