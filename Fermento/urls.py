"""
URL configuration for Fermento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.i18n import set_language
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    #Temporary until homepage exists
    path("", RedirectView.as_view(url='/recipe_manager')),
    
    path("recipe_manager/", include("Apps.recipe_manager.urls")),
    path("batches/", include("Apps.batches.urls")),
    path("settings/", include("Apps.settings_manager.urls")),
    path("api/", include("Apps.restapi_manager.urls")),

    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("admin/", admin.site.urls),
    path('set-language/', set_language, name='set_language'),   
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)