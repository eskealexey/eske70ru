from django.urls import path

from .views import view_projects, add_comment, ProjectDetailView
urlpatterns = [
    path('view/', view_projects, name='view_projects'),
    # path('view/<str:slug>/', project_detail, name='project_detail'),
    # path('project/<int:project_id>/comment/', add_comment, name='add_comment'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_id>/comment/', add_comment, name='add_comment'),
    ]