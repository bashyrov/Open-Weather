import datetime
from django.db import models
from django.utils import timezone


class City(models.Model):
    city_name = models.CharField('City Name', max_length=50, default="")
    day = models.DateField('Day', default=datetime.date.today)
    temperature = models.FloatField('Temperature', default=0.0)
    humidity = models.IntegerField('Humidity', default=0)
    condition = models.CharField('Condition', max_length=25, default="")
    rain_chance = models.IntegerField('Chance of Rain', default=0)
    weekly_forecast = models.JSONField('Weekly Forecast', default=dict)
    last_updated = models.DateTimeField(auto_now=True)
    day_updated_at = models.DateTimeField('Day Info Updated At', auto_now=True)
    week_updated_at = models.DateTimeField('Week Info Updated At', auto_now=True)

    def update_weekly_forecast(self, new_forecast):
        current_forecast = self.weekly_forecast
        if isinstance(current_forecast, dict):
            current_forecast.update(new_forecast)
        else:
            current_forecast = new_forecast
        self.weekly_forecast = current_forecast
        self.week_updated_at = timezone.now()
        self.save()

    def update_daily_info(self, temperature, humidity, condition, rain_chance):
        self.temperature = temperature
        self.humidity = humidity
        self.condition = condition
        self.rain_chance = rain_chance
        self.day_updated_at = timezone.now()
        self.save()

    def delete_past_data(self):
        today = timezone.now().date().isoformat()
        updated_forecast = {
            day: data for day, data in self.weekly_forecast.items() if day >= today
        }
        self.weekly_forecast = updated_forecast
        self.save()

    def __str__(self):
        return f"Temperature in {self.city_name} is {self.temperature} °C"

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
