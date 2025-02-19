from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, activate, confirm_email, login_view, logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
#--------------------восстановление пароля-----------------------------------------
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
