from django.contrib import admin

# Register your models here.

from .models import recipe

admin.site.register(recipe)