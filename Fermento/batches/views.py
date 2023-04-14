from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    context = {
    }
    return render(request, "batches/batches/overview.html", context)

def qrcode_overview(request):
    context = {
    }
    return render(request, "batches/qrcodes/overview.html", context)

def calender_overview(request):
    context = {
    }
    return render(request, "batches/calender/overview.html", context)
