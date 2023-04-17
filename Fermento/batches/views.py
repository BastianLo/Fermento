from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Batch, QrCode
import os
import math

@login_required(login_url='/accounts/login/')
def batches_all(request):
    #TODO: Limit should be a parameter
    LIMIT = 10
    uid = request.session['_auth_user_id']
    batches = Batch.objects.filter(owner=uid)
    count = len(batches)
    orderby = request.GET.get("orderby")
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    if orderby:
        try:
            desc = "-" if request.GET.get("direction") == "desc" else ""
            batches = batches.order_by(desc + orderby)
        except:
            print(f"Error: '{orderby}' attribute does not exist for object Batch")
    batches = batches[(page-1)*LIMIT:(page-1)*LIMIT+LIMIT]
    context = {
        "batches": batches,
        "order_items": ["name", "start_date"],
        "order_directions": ["asc", "desc"],
        "pages": {"current": page, "previous": max(page-1, 1), "next": max(1,min(page+1, math.ceil(count/LIMIT)))}
    }
    return render(request, "batches/batches/overview.html", context)

@login_required(login_url='/accounts/login/')
def batch_by_id(request, batch_id):
    uid = request.session['_auth_user_id']
    requested_batch = Batch.objects.filter(owner=uid, id=batch_id).first()
    if not requested_batch:
        raise Http404("Batch does not exist")
    context = {
        "batch":requested_batch,
    }
    return render(request, "batches/batches/details.html", context)

@login_required(login_url='/accounts/login/')
def qrcode_overview(request):
    uid = request.session['_auth_user_id']
    context = {
        "qrcodes": QrCode.objects.filter(owner=uid)
    }
    return render(request, "batches/qrcodes/overview.html", context)

@login_required(login_url='/accounts/login/')
def qrcode_by_id(request, qrcode_id):
    uid = request.session['_auth_user_id']
    requested_qrcode = QrCode.objects.filter(owner=uid, id=qrcode_id).first()
    if not requested_qrcode:
        raise Http404("Qrcode does not exist")
    app_url = os.getenv("APP_URL") if "APP_URL" in os.environ else "127.0.0.1"
    context = {
        "qrcode":requested_qrcode,
        "redirect_url": app_url + "/batches/qrcode/" + str(requested_qrcode.batch.id) + "/redirect"
    }
    return render(request, "batches/qrcodes/details.html", context)

@login_required(login_url='/accounts/login/')
def redirect_qrcode_by_id(request, qrcode_id):
    uid = request.session['_auth_user_id']
    requested_qrcode = QrCode.objects.filter(owner=uid, id=qrcode_id).first()
    if not requested_qrcode:
        raise Http404("Qrcode does not exist")
    return redirect(requested_qrcode.get_url())

@login_required(login_url='/accounts/login/')
def calender_overview(request):
    context = {
    }
    return render(request, "batches/calender/overview.html", context)
