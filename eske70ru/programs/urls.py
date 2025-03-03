from django.urls import path

from .views import view_programs, program_detail, download_program

urlpatterns = [
    path('view/', view_programs, name='view_programs'),
    path('<int:program_id>/', program_detail, name='program_detail'),
    path('download/<int:program_id>/', download_program, name='download_program'),
]
