from django.shortcuts import render, redirect
from .forms import CitySearchForm
from .models import City
from django.contrib import messages
from city_forecast import get_weather, save_weekly_data


def city_detail(request, city_name):
    save_weekly_data(city_name)
    city = City.objects.filter(city_name=city_name).first()
    return render(request, 'main/city_detail.html', {
        'city_name': city_name.title(), 'city': city})


def index(request):
    cities = ['New York', 'London', 'Kyiv']
    save_weekly_data(cities)
    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name'].title()
            if get_weather(city_name, "current"):
                return redirect('main:city_detail', city_name=city_name)
            else:
                form.add_error(None, "Please, provide a valid data.")
                messages.error(request, "Please, provide a valid data.")
    else:
        form = CitySearchForm()
    weather_data = City.objects.filter(city_name__in=cities)
    context = {
        'weather_data': weather_data,
        'form': form
    }
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')

