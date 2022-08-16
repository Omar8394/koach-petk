"""KOACH_PETK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve



urlpatterns = [
    path("", include("modulesApp.DashboardPortal.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path("", include("modulesApp.App.urls")),
    path("", include("modulesApp.Comunication.urls")),
    path("Planning/", include("modulesApp.Planning.urls", namespace="planning")),
    path("Helping/", include("modulesApp.Helping.urls", namespace="helping")),
    path("security/", include("modulesApp.Security.urls",namespace="security")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('admin/', admin.site.urls),
    
]
