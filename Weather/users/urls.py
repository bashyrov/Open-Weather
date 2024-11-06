from django.urls import path
from .views import login, registration, dashboard

app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('dashboard', dashboard, name='dashboard'),
]
