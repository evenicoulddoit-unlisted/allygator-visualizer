import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import randomColor from 'randomcolor';
import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';
import 'rxjs/add/observable/timer';
import 'rxjs/add/operator/exhaustMap';

import * as conf from './conf';
import { environment } from '../environments/environment';


interface Vehicle {
  id: string;
  lat: number;
  lng: number;
  bearing: number;
  active: boolean;
  iconUrl: string;
}


/**
 * Vehicle service offering a subscription to vehicle location data.
 */
@Injectable()
class VehiclesService {
  private _observable: Observable<any>;
  private _vehicleColors = {};

  public constructor(private http: HttpClient) {
    this._observable = this._getObservable();
  }

  /**
   * Create and return a subscription to the vehicles observable.
   */
  public subscribe(...args: any[]): Subscription {
    return this._observable.subscribe(...args);
  }

  /**
   * Create an observable to retrieve the vehicles every 3 seconds at most.
   */
  public _getObservable(): Observable<Vehicle[]> {
    return Observable.timer(0, 3000).exhaustMap(() => this._getVehicles());
  }

  /**
   * Return a promise which will resolve with the active vehicles.
   */
  private _getVehicles(): Promise<Vehicle[]> {
    return this.http
      .get<any[]>(this._getEndpoint(), { params: { active: 'true' }})
      .toPromise()
      .then(vehicles => vehicles.map(vehicle => this._parseVehicle(vehicle)));
  }

  /**
   * Parse the given vehicle, giving it an icon to use on the map.
   */
  private _parseVehicle(vehicle: any): Vehicle {
    vehicle.iconUrl = this._getVehicleIcon(vehicle);
    return vehicle;
  }

  /**
   * Return a URL to be used as the vehicles icon on the map.
   *
   * The icon assigns the vehicle a unique color, and is rotated to represent
   * the current bearing of the vehicle.
   */
  private _getVehicleIcon(vehicle): string {
    const url = 'https://chart.apis.google.com/chart?chst=d_map_spin&chld=0.5';
    const color = this._getVehicleColor(vehicle);
    const bearing = vehicle.bearing || 0;
    return `${url}|${bearing}|${color}|1`;
  }

  /**
   * Get or create a color for the given vehicle.
   */
  private _getVehicleColor(vehicle): string {
    const { id } = vehicle;
    let color = this._vehicleColors[id];

    if (!color) {
      color = this._vehicleColors[id] = randomColor().slice(1);
    }

    return color;
  }

  /**
   * Return the endpoint to request the vehicles from.
   */
  private _getEndpoint(): string {
    return `${environment.apiRoot}vehicles`;
  }
}


export { Vehicle, VehiclesService };
