from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("notification/", views.notifcation, name="index"),
    path("notification/save", views.notifcation_save, name="index"),
]