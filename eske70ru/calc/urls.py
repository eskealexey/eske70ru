from django.urls import path
from .views import zakon_oma

urlpatterns = [
    path('oma', zakon_oma, name='zakon_oma'),
    # path('about/', views.about, name='about'),
    # другие маршруты
]