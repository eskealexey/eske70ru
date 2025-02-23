from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_programs, program_detail

urlpatterns = [
    path('view/', view_programs, name='view_programs'),
    path('program/<int:program_id>/', program_detail, name='program_detail'),
]
