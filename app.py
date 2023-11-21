from flask import Flask
from weather import Weather

app = Flask('weather')
api_url = 'https://api.weather.gov'
location = '40.7703236,-79.9416973'
 
@app.route('/')
def index():
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    ret = '<p>Welcome to Our Weather App</p>'
    temp = wx.current_temp(location)
    wind = wx.current_wind(location)
    windChill = wx.current_windChill(location)
    visibility = wx.current_visibility(location)

    ret += '\n'
    ret += f"<p>Your current temperature is {temp['fahrenheit']}F"
    ret += '\n'
    ret += f"</br>Wind is blowing at {wind['speed_mph']}mph causing a wind chill of {windChill['windchill_degC']}C"
    ret += '\n'
    ret += f"</br>Visibility is {visibility['visibility_m']}m"
    ret += '</p>'

    return ret
