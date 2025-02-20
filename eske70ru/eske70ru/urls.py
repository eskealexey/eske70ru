"""
URL configuration for eske70ru project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from eske70ru import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('programs/', include('programs.urls')),
    # path('accounts/profile/', include('main.urls')),
    # path('accounts/profile/edit/', include('main.urls')),
    # path('accounts/profile/delete/', include('main.urls')),
    # path('accounts/profile/change_password/', include('main.urls')),
    # path('accounts/profile/change_email/', include('main.urls')),
    # path('accounts/profile/change_username/', include('main.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
