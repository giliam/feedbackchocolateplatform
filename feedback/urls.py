"""feedback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import protocole1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("protocole1/", include("protocole1.urls")),
    path("accounts/login/", protocole1.views.log_in, name="users.log_in"),
    path("accounts/logout/", protocole1.views.log_out, name="users.log_out"),
]