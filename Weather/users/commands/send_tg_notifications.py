from django.core.management.base import BaseCommand
from django.utils import timezone
from Weather.users.models import User
from Weather.users.telegram_bot import bot
from Weather.main.views import get_weather


class Command(BaseCommand):
    help = "Send weather notifications to users"

    def handle(self, *args, **kwargs):
        now = timezone.localtime()
        users = User.objects.exclude(tg_username="").filter(del_time__isnull=False)

        for user in users:
            if user.del_time.hour == now.hour and user.del_time.minute == now.minute:
                city_name = user.users_city
                forecast_data = get_weather(city_name, 'forecast', 1)
                message = self.format_weather_message(forecast_data, user.tg_username)
                bot.send_message(user.tg_username, message)
                self.stdout.write(self.style.SUCCESS(f"Sent notification to {user.tg_username}"))

    def format_weather_message(self, forecast_data, username):
        message = f'Good morning, {username}!\n'
        for city, data in forecast_data.items():
            message += f"🌆 Weather forecast for {city}:\n"
            avg_temp = data.get('avg_temp', 'N/A')
            condition = data.get('condition', 'N/A')
            humidity = data.get('humidity', 'N/A')
            rain_chance = data.get('rain_chance', 'N/A')
            message += f"Average temperature: {avg_temp}°C\n"
            message += f"Conditions: {condition}\n"
            message += f"Humidity: {humidity}%\n"
            message += f"Chance of rain: {rain_chance}%\n\n"
        return message