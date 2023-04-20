from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("notification/", views.notifcation, name="notifcation"),
    path("notification/save", views.notifcation_save, name="notifcation_save"),
]