/**
 * Map confugration
 */
interface Coords {
  lat: number;
  lng: number;
}

interface MapConfig {
  center: Coords;
  zoom: number;
}

const CITY_CENTER_LNG = 13.403;
const CITY_CENTER_LAT = 52.53;
const CITY_CENTER: Coords = { lat: CITY_CENTER_LAT, lng: CITY_CENTER_LNG };

const MAP_CONFIG: MapConfig = {
  center: CITY_CENTER,
  zoom: 13
};

export { MapConfig, MAP_CONFIG };
