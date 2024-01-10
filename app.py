import base64
from io import BytesIO
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, url_for
from matplotlib.figure import Figure
from weather import Weather

app = Flask('weather')
bootstrap = Bootstrap5(app)

api_url = 'https://api.weather.gov'
default_location = '40.7703236,-79.9416973'
 
@app.route('/', methods=['GET', 'POST'])
def index():
    location = default_location
    wx = Weather(api_url, 'C50501-SJHS Weather Application V1.0')
    if request.method == 'POST':
        location = request.form.get('location')
        #perform input validation
        location = location.split(',')
        if len(location) != 2:
            ret = '<h2>Location data must be in the form of "lat,lon"</h2>'
            ret += f"<a href=\"{url_for('index')}\">Go Back</a>"
            return ret
        try:    
            location = [float(l) for l in location]
        except TypeError:
            ret = '<h2>Location data must be in the form of "lat,lon" as decimals</h2>'
            ret += f"<a href=\"{url_for('index')}\">Go Back</a>"
            return ret
        location = [str(l) for l in location]
        location = ','.join(location)
        print(location)

    temp = wx.current_temp(location)
    wind = wx.current_wind(location)
    windChill = wx.current_windChill(location)
    visibility = wx.current_visibility(location)

    return render_template('main.html',temp=temp,wind=wind,windChill=windChill,visibility=visibility)


@app.route('/history')
def history():
    location = default_location
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