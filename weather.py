# my location is 40.7703236,-79.9416973

import json
import requests
import math
 
class Weather(object):
    def __init__(self, api_url, user_agent):
        self.api_url = api_url
        self.headers = {
            'User-Agent': user_agent,
            'content-type': 'application/json',
            'Accept': 'application/json'
        }


    def current_temp(self, location):
        latest = self._latest_observations(location)
        t = latest['temperature']['value']
        try:
            t = math.floor(t)
            f = float((9/5 * t) + 32)
            f = math.floor(f)
        except TypeError:
            t = None
            f = None

        #print(f"celsius temperature: {t}°, fahrenheit temperature: {f}°")
        ret = {
            'fahrenheit': f,
            'celsius': t
        }
        return ret

    def current_windChill(self, location):
        latest = self._latest_observations(location)
        try:
            wc = latest['windChill']['value']
        except TypeError:
            wc = None

        ret = {
            'windchill_degC': wc
        }
        return ret

    def current_wind(self, location):
        latest = self._latest_observations(location)
        try:
            dir = latest['windDirection']['value']
        except TypeError:
            dir = None
        #direction_cardinal = # do some magic
        try:
            speed = latest['windSpeed']['value']
            speed_mph = speed * 0.621371
        except TypeError:
            speed = None
            speed_mph = None
        try:
            gust = latest['windGust']['value']
            gust_mph = gust * 0.621371
        except TypeError:
            gust = None
            gust_mph = None

        ret = {
            'direction_degrees': dir,
            # 'direction_cardinal'
            'speed_kmh': speed,
            'speed_mph': speed_mph,
            'gust_kmh': gust,
            'gust_mph': gust_mph
        }
        return ret

    def current_visibility(self, location):
        latest = self._latest_observations(location)
        try:
            vis = latest['visibility']['value']
        except TypeError:
            vis = None

        ret = {
            'visibility_m': vis
        }
        return ret


    def _get_station(self, location=None):
        # get the info for location
        if not location:
            raise RuntimeError('No location spefified for call')
        
        url = f"{self.api_url}/points/{location}"
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            raise RuntimeError(f"API request failed: {res.reason} ({res.code})")
        data = res.json()
        url = data['properties']['observationStations']
        # get the nearest observation station for our location

        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            raise RuntimeError(f"API request failed for observation stations: {res.reason} ({'res.status_code'})")
        data = res.json()
        stations = data['features']
        station_id = stations[0]['properties']['stationIdentifier']
        return station_id


    def _latest_observations(self, location=None):
        if not location:
            raise RuntimeError('No location specified for call')
        station = self._get_station(location)


        url = f"{self.api_url}/stations/{station}/observations/latest"
        print(url)
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            raise RuntimeError(f"Unable to get latest observations: {res.reason} ({res.status_code})")
        #print(res.status_code)
        #print(res.text)
        data = res.json()
        return data['properties']



if __name__ == '__main__':
    api_url = 'https://api.weather.gov'
    location = '40.7703236,-79.9416973'
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    temp = wx.current_temp(location)
    print(temp)

    windChill = wx.current_windChill(location)
    print(windChill)

    wind = wx.current_wind(location)
    print(wind)

    visibility = wx.current_visibility(location)
    print(visibility)
