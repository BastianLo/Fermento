from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import recipe, process, process_schedule, process_step, utensils, recipe_ingredient, timedelta
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
        raise Http404("Recipe does not exist")
    context = {
        "recipe": selected_recipe,
        "show_empty_process_categories": settings.SHOW_EMPTY_PROCESS_CATEGORIES,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/accounts/login/')
def delete_recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    recipe.objects.filter(id=recipe_id, owner=uid).first().delete()
    return redirect(index)

@login_required(login_url='/accounts/login/')
def recipe_create(request):
    if request.method == "GET":
        return recipe_create_get(request)
    elif request.method == "POST":
        return recipe_create_post(request)

def recipe_create_get(request):
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
        print(p["utils"])
        print(p["ingredients"])
        new_process = process()
        new_process.owner = o
        new_process.name = p["name"]
        new_process.related_recipe = new_recipe
        new_process.save()
        for i in p["ingredients"]:
            new_ingredient = recipe_ingredient()
            new_ingredient.name = i["name"]
            new_ingredient.amount = i["amount"]
            new_ingredient.unit = i["unit"]
            new_ingredient.owner = o
            new_ingredient.related_process = new_process
            new_ingredient.save()
        for i in p["utils"]:
            new_util = utensils()
            new_util.name = i["name"]
            new_util.owner = o
            new_util.related_process = new_process
            new_util.save()
        for count, ps in enumerate(p["steps"]):
            new_step = process_step()
            new_step.text = ps["text"]
            new_step.owner = o
            new_step.index = count
            new_step.related_process = new_process
            new_step.save()
        for s in p["schedules"]:
            new_schedule = process_schedule()
            new_schedule.related_process = new_process
            new_schedule.executed_once = s["runOnce"]
            new_schedule.start_time = timedelta(minutes=_input_to_deltatime(s["start"]))
            new_schedule.wait_time = timedelta(minutes=_input_to_deltatime(s["frequency"]))
            new_schedule.end_time = timedelta(minutes=_input_to_deltatime(s["end"]))
            new_schedule.save()
    
    return JsonResponse({'status':'success', 'recipe_id':new_recipe.id})


def not_found(request, e):
    print(e)
    return render(request, "recipe_manager/recipe_notfound_error.html")


def _input_to_deltatime(input_string):
    total_minutes = 0
    if len(input_string.split(" ")) > 1:
        days = input_string.split(" ")[0]
        time = input_string.split(" ")[1]
        total_minutes += (int(days) * 24 * 60)
    else:
        time = input_string.split(" ")[0]
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1])
    total_minutes += hours * 60
    total_minutes += minutes
    return total_minutes

    