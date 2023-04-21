from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import SettingsNotification


# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    context = {
    }
    return render(request, "settings_manager/index.html", context)


@login_required(login_url='/accounts/login/')
def notification(request):
    settings, created = SettingsNotification.objects.get_or_create(user=request.user)
    context = {
        "settings": settings
    }
    return render(request, "settings_manager/notification.html", context)


@login_required(login_url='/accounts/login/')
def notification_save(request):
    if request.method != 'POST':
        return redirect(notification)
    setting = SettingsNotification.objects.filter(user=request.user).first()

    setting.pushover_enabled = request.POST.get('pushover_enabled', '') == 'on'
    setting.pushover_user_token = request.POST.get('pushover_user_key', '')
    setting.pushover_app_token = request.POST.get('pushover_app_key', '')
    setting.save()

    return redirect(notification)
