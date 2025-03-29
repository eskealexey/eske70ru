from django.urls import path

from .views import view_projects, project_detail
urlpatterns = [
    path('view/', view_projects, name='view_projects'),
    path('view/<str:slug>/', project_detail, name='project_detail'),
    ]