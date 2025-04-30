import requests
from datetime import timedelta
from django.utils import timezone
from main.models import City

time_slots = {
    '00:00': 'Midnight',
    '06:00': 'Morning',
    '12:00': 'Afternoon',
    '18:00': 'Evening',
}


def get_weather(city_name, request_type, days = None):  #request_type = 'current' or 'forecast'
    api_key = 'f74351ed3256444daf0102110240411'
    url = f'http://api.weatherapi.com/v1/{request_type}.json'
    params = {
        'key': api_key,
        'q': city_name,
        'days': days
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        forecast_data = response.json()
        weather_forecast = {city_name: {}}
        if request_type == 'forecast' and 'forecast' in forecast_data:
            for day in forecast_data['forecast']['forecastday']:
                date = day['date']
                avg_temp = day['day']['avgtemp_c']
                condition = day['day']['condition']['text']
                humidity = day['day']['avghumidity']
                rain_chance = day['day']['daily_chance_of_rain']
                hourly_data = {}
                for hour in day['hour']:
                    time_str = hour['time'].split(' ')[1]
                    for time_slot, period_name in time_slots.items():
                        if time_str == time_slot:
                            hourly_data[period_name] = {
                                'temp_c': hour['temp_c'],
                                'condition': hour['condition']['text'],
                                'humidity': hour['humidity'],
                                'rain_chance': hour.get('chance_of_rain', 0),
                            }
                weather_forecast[city_name][date] = {
                    'avg_temp': avg_temp,
                    'condition': condition,
                    'humidity': humidity,
                    'rain_chance': rain_chance,
                    'hourly': hourly_data
                }
        elif request_type == 'current' and 'current' in forecast_data:
            current = forecast_data['current']
            weather_forecast[city_name] = {
                'temp_c': current['temp_c'],
                'condition': current['condition']['text'],
                'humidity': current['humidity'],
                'rain_chance': current.get('precip_mm', 0),
            }
        return weather_forecast
    else:
        return None


def save_weekly_data(*args):
    if len(args) == 1 and isinstance(args[0], list):
        cities = args[0]
    else:
        cities = args
    for city_name in cities:
        city_object, created = City.objects.get_or_create(city_name=city_name)
        if not city_object.weekly_forecast or (timezone.now() - city_object.week_updated_at) > timedelta(minutes=1):
            city_object.delete_past_data()
            current_weather_data = get_weather(city_name, 'current')
            forecast_data = get_weather(city_name, 'forecast', 6)
            if current_weather_data:
                current_data = current_weather_data.get(city_name, {})
                city_object.update_daily_info(
                    temperature=current_data['temp_c'],
                    humidity=current_data['humidity'],
                    condition=current_data['condition'],
                    rain_chance=current_data.get('rain_chance', 0)
                )
            if forecast_data:
                forecast_data = forecast_data.get(city_name, {})
                upcoming_forecast = {}
                today = timezone.now().date().isoformat()
                if today in forecast_data:
                    today_data = forecast_data.pop(today)
                    upcoming_forecast[today] = {
                        'avg_temperature': today_data['avg_temp'],
                        'condition': today_data['condition'],
                        'humidity': today_data['humidity'],
                        'rain_chance': today_data['rain_chance'],
                        'hourly_forecast': {}
                    }
                    hourly_data = today_data['hourly']
                    for time_slot, period_name in time_slots.items():
                        if period_name in hourly_data:
                            upcoming_forecast[today]['hourly_forecast'][period_name] = {
                                'temp_c': hourly_data[period_name]['temp_c'],
                                'condition': hourly_data[period_name]['condition'],
                                'humidity': hourly_data[period_name]['humidity'],
                                'rain_chance': hourly_data[period_name]['rain_chance']
                            }

                for i, (day, data) in enumerate(forecast_data.items()):
                    if i >= 6:
                        break

                    upcoming_forecast[day] = {
                        'avg_temperature': data['avg_temp'],
                        'condition': data['condition'],
                        'humidity': data['humidity'],
                        'rain_chance': data['rain_chance'],
                        'hourly_forecast': data['hourly']
                    }

                city_object.update_weekly_forecast(upcoming_forecast)
            else:
                print(f"Failed to retrieve data for the city {city_name}.")