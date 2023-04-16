from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from .models import settings_notification

@login_required(login_url='/accounts/login/')
def index(request):
    context = {
    }
    return render(request, "settings_manager/index.html", context)

@login_required(login_url='/accounts/login/')
def notifcation(request):
    settings, created = settings_notification.objects.get_or_create(user=request.user)
    context = {
        "settings": settings
    }
    return render(request, "settings_manager/notification.html", context)

@login_required(login_url='/accounts/login/')
def notifcation_save(request):
    setting = settings_notification.objects.filter(user=request.user).first()

    setting.pushover_enabled = request.POST.get('pushover_enabled', '') == 'on'
    setting.pushover_user_token = request.POST.get('pushover_user_key', '')
    setting.pushover_app_token = request.POST.get('pushover_app_key', '')
    setting.save()

    return redirect(notifcation)