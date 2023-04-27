import json
import math
import os

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Batch, QrCode, Execution, JournalEntry
from ..recipe_manager.modules.parser import downsize_image


@login_required(login_url='/accounts/login/')
def batches_all(request):
    # TODO: Limit should be a parameter
    limit = 10
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
    batches = batches[(page - 1) * limit:(page - 1) * limit + limit]
    context = {
        "batches": batches,
        "order_items": ["name", "start_date"],
        "order_directions": ["asc", "desc"],
        "pages": {"current": page, "previous": max(page - 1, 1),
                  "next": max(1, min(page + 1, math.ceil(count / limit)))}
    }
    return render(request, "batches/batches/overview.html", context)


@login_required(login_url='/accounts/login/')
def batch_by_id(request, batch_id):
    if "complete" in request.POST:
        if Execution.objects.filter(id=request.POST["complete"], owner=request.user).exists():
            Execution.objects.filter(id=request.POST["complete"], owner=request.user).first().archive()
    uid = request.session['_auth_user_id']
    requested_batch = Batch.objects.filter(owner=uid, id=batch_id).first()
    if not requested_batch:
        raise Http404("Batch does not exist")
    context = {
        "batch": requested_batch,
        "batch_json": json.loads(serializers.serialize('json', [requested_batch, ]))[0],
    }
    return render(request, "batches/batches/details.html", context)


@login_required(login_url='/accounts/login/')
def execute_execution_by_id(request, execution_id):
    try:
        if Execution.objects.filter(id=int(execution_id), owner=request.user).exists():
            Execution.objects.filter(id=int(execution_id), owner=request.user).first().archive()
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"status": "Internal Server error"}, status=500)


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
        "qrcode": requested_qrcode,
        "redirect_url": (app_url + "/batches/qrcode/" + str(
            requested_qrcode.id) + "/redirect") if requested_qrcode.batch else ""
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


@login_required(login_url='/accounts/login/')
def create_journal_entry(request):
    json_journal_data = json.loads(request.POST["journalEntry"])
    journal_entry = JournalEntry.objects.create(created_datetime=timezone.now(), owner=request.user,
                                                related_batch_id=request.POST["batchId"])
    journal_entry.title = json_journal_data["name"]
    journal_entry.description = json_journal_data["description"]
    if "image" in request.FILES:
        journal_entry.image = downsize_image(request.FILES["image"])
    journal_entry.save()
    return JsonResponse({"status": "test"}, status=200)
