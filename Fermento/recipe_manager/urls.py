from django.urls import path

from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe_by_id, name="recipe_by_id"),
    path("recipe/<int:recipe_id>/delete", views.delete_recipe_by_id, name="delete_recipe_by_id"),
    path("recipe/create", views.recipe_create, name="recipe_by_id"),
]
handler404 = 'recipe_manager.views.not_found'