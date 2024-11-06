from django.urls import path
from .views import index, about, city_detail


app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    path('explore-us', about, name='about'),
    path('city/<str:city_name>/', city_detail, name='city_detail')
]
