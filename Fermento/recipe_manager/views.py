from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from .models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):
    recipes = recipe.objects.filter(owner=request.session['_auth_user_id'])
    context = {
        "recipes": recipes
    }
    return render(request, "recipe_manager/index.html", context)

@login_required(login_url='/accounts/login/')
def recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    selected_recipe = recipe.objects.filter(id=recipe_id, owner=uid).first()
    if selected_recipe:
        template = loader.get_template("recipe_manager/recipe.html")
    else:
        template = loader.get_template("recipe_manager/recipe_notfound_error.html")
        raise Http404("Recipe does not exist")
    context = {
        "recipe": selected_recipe,
    }
    return HttpResponse(template.render(context, request))

def not_found(request, e):
    return render(request, "recipe_manager/recipe_notfound_error.html")
