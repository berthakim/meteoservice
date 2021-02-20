from django.shortcuts import render

def weather_js(request):
	return render(request, 'weather_js/weather_js.html')
