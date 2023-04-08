from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(recipe)
admin.site.register(recipe_ingredient)
admin.site.register(process_step)
admin.site.register(process)
