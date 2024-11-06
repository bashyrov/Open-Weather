from django.contrib import admin
from .models import City


@admin.register(City)
class WeeklyForecastAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'day', 'temperature', 'humidity', 'condition', 'last_updated', 'day_updated_at', 'week_updated_at')

