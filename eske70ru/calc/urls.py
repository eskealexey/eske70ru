from django.urls import path
from .views import zakon_oma, calculation_of_resistor_voltage_divider

urlpatterns = [
    path('oma', zakon_oma, name='zakon_oma'),
    path('voltagedivider', calculation_of_resistor_voltage_divider, name='voltagedivider'),
    # path('about/', views.about, name='about'),
    # другие маршруты
]