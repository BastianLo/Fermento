from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

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
        "show_empty_process_categories": settings.SHOW_EMPTY_PROCESS_CATEGORIES,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/accounts/login/')
def recipe_create(request):
    if request.method == "GET":
        return recipe_create_get(request)
    elif request.method == "POST":
        return recipe_create_post(request)

def recipe_create_get(request):
    uid = request.session['_auth_user_id']
    template = loader.get_template("recipe_manager/components/create_recipe.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

def recipe_create_post(request):
    uid = request.session['_auth_user_id']
    o = User.objects.get(id=uid)
    data = request.POST.dict()

    new_recipe = recipe()
    new_recipe.owner = o
    new_recipe.name = data["name"]
    new_recipe.description = data["description"]
    new_recipe.image = request.FILES["image"]
    new_recipe.difficulty = data["difficulty"]
    new_recipe.save()

    processes = json.loads(request.POST.dict()["processes"])
    for p in processes:
        new_process = process()
        new_process.owner = o
        new_process.name = p["name"]
        new_process.related_recipe = new_recipe
        new_process.save()
        for i in p["ingredients"]:
            new_ingredient = recipe_ingredient()
            new_ingredient.name = i["name"]
            new_ingredient.amount = i["amount"]
            new_ingredient.unit = i["amount"]
            new_ingredient.owner = o
            new_ingredient.related_process = new_process
            new_ingredient.save()
        for count, ps in enumerate(p["steps"]):
            new_step = process_step()
            new_step.text = ps["text"]
            new_step.owner = o
            new_step.index = count
            new_step.related_process = new_process
            new_step.save()
    
    return JsonResponse({'status':'success'})


def not_found(request, e):
    return render(request, "recipe_manager/recipe_notfound_error.html")
