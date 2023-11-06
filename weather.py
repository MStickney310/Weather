

import json
import requests


class Weather(object):
    def __init__(self, api_url, user_agent):
        self.api_url = api_url
        self.headers = {
            'User-Agent': user_agent,
            'content-type': 'application/json',
            'Accept': 'application/json'
        }

    def temp(self, station):
        latest = self._latest_observations(station)

    def _latest_observations(self, station=None):
        if not station:
            raise RuntimeError('No station specified for call')
        url = f"{self.api_url}/stations/{station}/observations/latest"
        print(url)
        res = requests.get(url, headers=self.headers)
        print(res.status_code)
        print(res.text)
        return




if __name__ == '__main__':
    api_url = 'https://api.weather.gov'
    station = '0358W'
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    wx.temp(station)


