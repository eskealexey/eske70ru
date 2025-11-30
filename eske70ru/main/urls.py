import weather_api
from django.urls import path

from .views import index

urlpatterns = [
    path('', index, name='home'),
]


