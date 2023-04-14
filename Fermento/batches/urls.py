from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("batch", views.index, name="index"),
    path("qrcode", views.qrcode_overview, name="qrcode_overview"),
    path("calender", views.calender_overview, name="calender_overview"),
]