from django.urls import path

from .views import register, activate, confirm_email

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('confirm_email/', confirm_email, name='confirm_email'),
]
