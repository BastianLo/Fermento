from django.contrib import admin

# Register your models here.

from .models import *
from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

#admin.site.register(recipe)
admin.site.register(recipe_ingredient)
admin.site.register(process_step)
admin.site.register(process)
admin.site.register(process_schedule)
admin.site.register(utensils)
admin.site.register(recipe, MyModelAdmin)