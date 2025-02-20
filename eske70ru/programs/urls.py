from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_programs

urlpatterns = [
    path('view/', view_programs, name='view_programs'),

]
