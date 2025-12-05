from django.urls import path
from .views import zakon_oma, calculation_of_resistor_voltage_divider, calculate_adc_value, adc_calculator

urlpatterns = [
    path('oma/', zakon_oma, name='zakon_oma'),
    path('voltagedivider/', calculation_of_resistor_voltage_divider, name='voltagedivider'),
    path('calcacp/',  adc_calculator, name='adc_calculator'),
    # другие маршруты
]