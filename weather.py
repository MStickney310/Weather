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


    def temp(self, location):
        latest = self._latest_observations(location)
        t = latest['temperature']['value']
        t = math.floor(t)
        f = float((9/5 * t) + 32)
        f = math.floor(f)
        print(f"celsius temperature: {t}°, fahrenheit temperature: {f}°")


    def windSpeed(self, location):
        latest = self._latest_observations(location)
        ws = latest['windSpeed']['value']
        print(f"Wind Speed: {ws}")


    def windChill(self, location):
        latest = self._latest_observations(location)
        wc = latest['windChill']['value']


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
        print(res.status_code)
        print(res.text)
        data = res.json()
        return data['properties']



if __name__ == '__main__':
    api_url = 'https://api.weather.gov'
    location = '40.7703236,-79.9416973'
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    wx.temp(location)


