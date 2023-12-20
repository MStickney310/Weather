import base64
from io import BytesIO
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from matplotlib.figure import Figure
from weather import Weather

app = Flask('weather')
bootstrap = Bootstrap5(app)

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

    #ret += '\n'
    #ret += f"<p>Your current temperature is {temp['fahrenheit']}F"
    #ret += '\n'
    #ret += f"</br>Wind is blowing at {wind['speed_mph']}mph causing a wind chill of {windChill['windchill_degC']}C"
    #ret += '\n'
    #ret += f"</br>Visibility is {visibility['visibility_m']}m"
    #ret += '</p>'

    return render_template('main.html',temp=temp,wind=wind,windChill=windChill,visibility=visibility)


@app.route('/history')
def history():
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    temps = wx.past_temps(location)

    fig = Figure()
    ax = fig.subplots()
    ax.plot([t['fahrenheit'] for t in temps])
    #save it to a temprorary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    #embed the result in the HTML output
    temp_graph = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return f"<img src='data:image/png;base64,{data}'/>"
    #return render_template('history.html')
    return render_template('history.html',temp_graph_img=temp_graph)