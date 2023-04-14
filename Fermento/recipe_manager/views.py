from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import recipe, process, process_schedule, process_step, utensils, recipe_ingredient, timedelta
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
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
def edit_recipe_by_id(request, recipe_id):
    if request.method == "GET":
        return edit_recipe_get(request, recipe_id)
    elif request.method == "POST":
        return edit_recipe_post(request, recipe_id)

@login_required(login_url='/accounts/login/')
def edit_recipe_get(request, recipe_id):
    uid = request.session['_auth_user_id']
    selected_recipe = recipe.objects.filter(id=recipe_id, owner=uid).first()
    template = loader.get_template("recipe_manager/components/edit_recipe.html")
    processes = json.loads(serializers.serialize('json', selected_recipe.get_processes()))
    for i, p in enumerate(processes):
        print(i)
        processes[i]["ingredients"] = serializers.serialize('json', recipe_ingredient.objects.filter(related_process=p["pk"]))
        processes[i]["process_steps"] = serializers.serialize('json', process_step.objects.filter(related_process=p["pk"]).order_by("index"))
        processes[i]["utils"] = serializers.serialize('json', utensils.objects.filter(related_process=p["pk"]))
        processes[i]["schedule"] = serializers.serialize('json', process_schedule.objects.filter(related_process=p["pk"]))
    context = {
        "recipe": selected_recipe,
        "recipe_json": serializers.serialize('json', [ selected_recipe, ]),
        "process_json": processes
    }
    return HttpResponse(template.render(context, request))


def edit_recipe_post(request, recipe_id):
    uid = request.session['_auth_user_id']
    o = User.objects.get(id=uid)
    data = request.POST.dict()

    new_recipe = recipe.objects.filter(id=recipe_id, owner=o)[0]
    new_recipe.owner = o
    new_recipe.name = data["name"]
    new_recipe.description = data["description"]
    if "image" in request.FILES:
        new_recipe.image = request.FILES["image"]
    new_recipe.difficulty = data["difficulty"]
    new_recipe.save()
    processes = json.loads(request.POST.dict()["processes"])
    db_processes = process.objects.filter(owner=o, related_recipe=new_recipe)
    delete_processes = [dbp.id for dbp in db_processes if dbp.id not in [int(p["id"]) for p in processes]]
    process.objects.filter(id__in=delete_processes).delete()
    for p in processes:
        if p["id"] == "-1":
            new_process = process()
            new_process.related_recipe = new_recipe
            new_process.owner = o
        else:
            new_process = process.objects.filter(id=p["id"], owner=o)[0]
        new_process.name = p["name"]
        new_process.save()

        #Delete ingredients that were removed by user
        db_ingredients = recipe_ingredient.objects.filter(owner=o, related_process=new_process)
        delete_ingredients = [dbi.id for dbi in db_ingredients if dbi.id not in [int(i["id"]) for i in p["ingredients"]]]
        recipe_ingredient.objects.filter(id__in=delete_ingredients).delete()
        #Delete Utensils that were removed by user
        db_utils = utensils.objects.filter(owner=o, related_process=new_process)
        delete_utils = [dbu.id for dbu in db_utils if dbu.id not in [int(u["id"]) for u in p["utils"]]]
        utensils.objects.filter(id__in=delete_utils).delete()
        #Delete Process steps that were removed by user
        db_steps = process_step.objects.filter(owner=o, related_process=new_process)
        delete_steps = [dbps.id for dbps in db_steps if dbps.id not in [int(ps["id"]) for ps in p["steps"]]]
        process_step.objects.filter(id__in=delete_steps).delete()
        #Delete Schedules that were removed by user
        db_schedules = process_schedule.objects.filter(owner=o, related_process=new_process)
        delete_schedules = [dbs.id for dbs in db_schedules if dbs.id not in [int(s["id"]) for s in p["schedules"]]]
        process_schedule.objects.filter(id__in=delete_schedules).delete()

        for i in p["ingredients"]:
            #TODO: Override recipe-index once implemented to save order changes
            if i["id"] == "-1":
                new_ingredient = recipe_ingredient()
                new_ingredient.related_process = new_process
                new_ingredient.owner = o
            else:
                new_ingredient = recipe_ingredient.objects.filter(owner=o, id=i["id"])[0]
            new_ingredient.name = i["name"]
            new_ingredient.amount = i["amount"]
            new_ingredient.unit = i["unit"]
            new_ingredient.save()
        for u in p["utils"]:
            if u["id"] == "-1":
                new_util = utensils()
                new_util.related_process = new_process
                new_util.owner = o
            else:
                new_util = utensils.objects.filter(owner=o, id=u["id"])[0]
            new_util.name = u["name"]
            new_util.save()
        for count, ps in enumerate(p["steps"]):
            print(count, ps)
            if ps["id"] == "-1":
                new_step = process_step()
                new_step.owner = o
                new_step.related_process = new_process
            else:
                new_step = process_step.objects.filter(owner=o, related_process=new_process, id=ps["id"])[0]
            new_step.text = ps["text"]
            new_step.index = count
            new_step.save()
        for s in p["schedules"]:
            if s["id"] == "-1":
                new_schedule = process_schedule()
                new_schedule.related_process = new_process
                new_schedule.owner = o
            else:
                new_schedule = process_schedule.objects.filter(owner=o, id=s["id"], related_process=new_process)[0]
            new_schedule.executed_once = s["runOnce"]
            new_schedule.start_time = timedelta(minutes=_input_to_deltatime(s["start"]))
            new_schedule.wait_time = timedelta(minutes=_input_to_deltatime(s["frequency"]))
            new_schedule.end_time = timedelta(minutes=_input_to_deltatime(s["end"]))
            new_schedule.save()
    
    return JsonResponse({'status':'success', 'recipe_id':new_recipe.id})

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
    if "image" in request.FILES:
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
            new_schedule.owner = o
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
    if str(input_string).isdigit():
        total_minutes += int(input_string) * 24 * 60
        return total_minutes
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

    