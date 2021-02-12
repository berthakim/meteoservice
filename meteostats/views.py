from django.shortcuts import render

def meteostats(request):
    return render(request, 'meteostats/meteostats.html')
