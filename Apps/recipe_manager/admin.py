from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import *


# Register your models here.

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(RecipeIngredient)
admin.site.register(ProcessStep)
admin.site.register(Process)
admin.site.register(ProcessSchedule)
admin.site.register(Utensils)
admin.site.register(Recipe, MyModelAdmin)
