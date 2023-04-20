from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

urlpatterns = [
    path("", RedirectView.as_view(url='recipe')),
    path("recipe/", views.index, name="recipeindex"),
    path("recipe/<int:recipe_id>/", views.recipe_by_id, name="recipe_by_id"),
    path("recipe/<int:recipe_id>/delete", views.delete_recipe_by_id, name="delete_recipe_by_id"),
    path("recipe/<int:recipe_id>/edit", views.edit_recipe_by_id, name="edit_recipe_by_id"),
    path("recipe/<int:recipe_id>/execute", views.execute_recipe_by_id, name="execute_recipe_by_id"),
    path("recipe/<int:recipe_id>/export", views.export_recipe_by_id, name="export_recipe_by_id"),
    path("recipe/import", views.import_recipe, name="import_recipe"),
    path("recipe/create", views.recipe_create, name="recipe_by_id"),
]
handler404 = 'recipe_manager.views.not_found'