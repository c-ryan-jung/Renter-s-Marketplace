"""techrent URL Configuration

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
from django.urls import path, re_path, include
from app import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/all_devices', views.all_devices),
    path('api/userFromAuth', views.getUserFromAuth),
    path('api/updateRecs', views.updateRecs),
    re_path(r'^api/transaction/(?P<uniqueID>[0-9]+)$', views.ViewOrUpdateTransaction),
    re_path(r'^api/device/(?P<uniqueID>[0-9]+)$', views.ViewOrUpdateDevice),
    re_path(r'^api/user/(?P<uniqueID>[0-9]+)$', views.ViewOrUpdateUser),

    re_path(r'^api/user/(?P<uniqueID>[0-9]+)/delete$', views.DeleteUser),
    re_path(r'^api/transaction/(?P<uniqueID>[0-9]+)/delete$', views.DeleteTransaction),
    re_path(r'^api/device/(?P<uniqueID>[0-9]+)/delete$', views.DeleteDevice),

    re_path(r'^api/user/create$', views.createUser),
    re_path(r'^api/transaction/create$', views.createTransaction),
    re_path(r'^api/device/create$', views.createDevice),
    re_path(r'^create/authentication', views.CreateAuthentication),
    re_path(r'^logout', views.logout),

    re_path(r'^api/getRecs/(?P<id>[0-9]+)$', views.getRecs)
]
