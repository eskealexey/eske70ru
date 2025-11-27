from django.urls import path

from .views import view_projects, add_comment, ProjectDetailView, ProjectFileDownloadView
urlpatterns = [
    path('view/', view_projects, name='view_projects'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_id>/comment/', add_comment, name='add_comment'),
    path('<int:file_id>', ProjectFileDownloadView.as_view(), name='project_file_download'),
    ]