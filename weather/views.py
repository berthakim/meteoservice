from django.shortcuts import render
from .models import Light
from requests import get
import json
import folium
import os
import webbrowser
import html
from datetime import datetime

# string represention of date
timestamp = 1528797322
date_time = datetime.fromtimestamp(timestamp).now()

# weather from OpenWeatherMap api
url = 'API key'

stations = get(url).json()

temps, pres, humid, wind, desc, icon = [], [], [], [], [], []
tmax = 0.0
tmin = 100.0
lons = [station['coord']['lon'] for station in stations['list']]
lats = [station['coord']['lat'] for station in stations['list']]
wsnames = [html.escape(station['name']) for station in stations['list']]
for data in stations['list']:
    t = data['main']['temp']
    p = data['main']['pressure']
    h = data['main']['humidity']
    w = data['wind']['speed']
    d = data['weather'][0]['description']
    i = data['weather'][0]['icon']
    temps.append(str(t))
    pres.append(str(p))
    humid.append(str(h))
    wind.append(str(w))
    desc.append(str(d))
    icon.append(str(i))

# TODO: to delete?
def colourgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    r = 255 - b - g
    hexcolour = '#%02x%02x%02x' % (r,g,b)
    return hexcolour

def weather_map(request):
    m = folium.Map(location=[47.5, 2.5], zoom_start=9)
    # access to the data from DB (light and imgs_light)
    lights = Light.objects.all()
    # define the current date (day and month) for compare to the Light
    today = datetime.now()
    today_day, today_month = today.day, today.month
    # today's date in str to show inside of the popups
    today_str = date_time.strftime("%d %B %Y")
    for n in range(len(lons)-1):
        hcol = colourgrad(tmin, tmax, float(temps[n]))  # TODO: to delete?
        html=f'''
        {today_str}
        <!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> -->
        <script src='https://kit.fontawesome.com/a076d05399.js'></script>
        <h3>{wsnames[n]}</h3>
        <p>{temps[n]} °C <i class="fas fa-sun" style="font-size:25px;color:black"></i> {desc[n]}</p>
        <p>Pressure: {pres[n]}</p>
        <p>Humidity: {humid[n]}</p>
        <p>Wind speed: {wind[n]} km/h</p>

            <!-- fas fa-cloud, fas fa-cloud-meatball, fas fa-cloud-moon, fas fa-cloud-moon-rain-->
            <!-- fab fa-cloudversify, fas fa-cloud-sun, fas fa-cloud-sun-rain -->
            <!-- fas fa-cloud-rain, fas fa-cloud-showers-heavy -->
            <!-- fas fa-sun -->
            <!-- fas fa-wind -->

        '''
        iframe = folium.IFrame(html=html, width=500, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([lats[n], lons[n]],
                      radius = 5,
                      popup = popup).add_to(m)

    m = m._repr_html_()
    context = {'my_map': m, 'lights': lights, 'today_day': today_day, 'today_month': today_month}

    return render(request, 'weather/weather.html', context)
