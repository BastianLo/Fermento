from django.urls import path

from . import views

urlpatterns = [
    path("", views.batches_all, name="index"),
    path("batch/", views.batches_all, name="batch_all"),
    path("batch/<int:batch_id>/", views.batch_by_id, name="batch_by_id"),
    path("qrcode/", views.qrcode_overview, name="qrcode_overview"),
    path("qrcode/<int:qrcode_id>/", views.qrcode_by_id, name="qrcode_by_id"),
    path("qrcode/<int:qrcode_id>/redirect/", views.redirect_qrcode_by_id, name="redirect_qrcode_by_id"),
    path("calender/", views.calender_overview, name="calender_overview"),
]