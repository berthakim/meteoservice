# Django
# from django.shortcuts import render
# from plotly.offline import plot
# from plotly.graph_objs import Scatter

# def index(request):
#     x_data = [0,1,2,3]
#     y_data = [x**2 for x in x_data]
#     plot_div = plot([Scatter(x=x_data, y=y_data,
#                         mode='lines', name='test',
#                         opacity=0.8, marker_color='green')],
#                output_type='div')
#     return render(request, "index.html", context={'plot_div': plot_div})


# <!DOCTYPE HTML>
# <html>
# <head>
#   <meta charset="utf-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <title>test</title>
# </head>
# <body>
#   {% autoescape off %}
#   {{ plot_div }}
#   {% endautoescape %}
# </body>
# </html>

# source: https://www.codingwithricky.com/2019/08/28/easy-django-plotly/

from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter