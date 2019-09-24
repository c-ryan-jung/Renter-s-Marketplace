"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from macroservices import views
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    re_path(r'^details/(?P<id>[0-9]+)$', views.details),
    re_path(r"^logout", views.logout),
    re_path(r"^login", views.login),
    re_path(r"^create_account", views.create_account),
    path('create_listing', views.create_listing),
    path('search', views.search)
]
