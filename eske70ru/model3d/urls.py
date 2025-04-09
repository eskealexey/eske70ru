from django.urls import path

from .views import views

urlpatterns = [
    path('', views, name='view_3d'),

]