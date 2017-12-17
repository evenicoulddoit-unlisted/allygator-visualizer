import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';

import { MapConfig, MAP_CONFIG } from './conf';
import { Vehicle, VehiclesService } from './vehicles.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  public title = 'app';
  public map: MapConfig = MAP_CONFIG;
  public vehicles: Vehicle[] = [];
  public error = false;

  private _vehicleSubscription: Subscription;

  public constructor(private vehiclesService: VehiclesService) {}

  /**
   * When the component loads, subscribe to vehicle location updates.
   */
  public ngOnInit() {
    this._vehicleSubscription = (
      this.vehiclesService.subscribe(
        vehicles => this.vehicles = vehicles,
        () => this.error = true
      )
    );
  }

  public ngOnDestroy() {
    if (this._vehicleSubscription) {
      this._vehicleSubscription.unsubscribe();
    }
  }

  /**
   * Provide a track-by function, to prevent unnecessary DOM updates.
   */
  public trackByVehicle(index: number, vehicle: Vehicle): string {
    return vehicle.id;
  }
}
