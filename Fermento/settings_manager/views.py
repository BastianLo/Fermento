from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
    context = {
    }
    return render(request, "settings_manager/index.html", context)

@login_required(login_url='/accounts/login/')
def notifcation(request):
    context = {
    }
    return render(request, "settings_manager/notification.html", context)
