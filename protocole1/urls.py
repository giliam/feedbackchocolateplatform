from django.urls import path, re_path

from protocole1 import views

urlpatterns = [path("", views.homepage, name="homepage")]
