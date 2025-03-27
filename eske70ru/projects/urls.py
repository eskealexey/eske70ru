from django.urls import path

from .views import view_projects
urlpatterns = [
    path('view/', view_projects, name='view_projects'),
    ]