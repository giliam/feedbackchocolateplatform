from django.urls import path, re_path

from protocole1 import views

urlpatterns = [
    path("", views.homepage, name="protocole1.homepage"),
    re_path(
        r"experiment/(?P<experiment_id>[0-9]+)/",
        views.participate_experiment,
        name="protocole1.participate_experiment",
    ),
    re_path(
        r"experiment/results/(?P<experiment_id>[0-9]+)/",
        views.results_experiment,
        name="protocole1.results_experiment",
    ),
]
