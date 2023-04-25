import json
import math

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.dateparse import parse_duration

from .models import Recipe, Process, ProcessSchedule, ProcessStep, Utensils, RecipeIngredient
from .modules.parser import RecipeParser


@login_required(login_url='/accounts/login/')
def index(request):
    limit = 10
    recipes = Recipe.objects.filter(owner=request.user)
    count = len(recipes)
    orderby = request.GET.get("orderby")
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    if orderby:
        try:
            desc = "-" if request.GET.get("direction") == "desc" else ""
            recipes = recipes.order_by(desc + orderby)
        except:
            print(f"Error: '{orderby}' attribute does not exist for object Batch")
    recipes = recipes[(page - 1) * limit:(page - 1) * limit + limit]
    context = {
        "recipes": recipes,
        "order_items": ["name", "difficulty"],
        "order_directions": ["asc", "desc"],
        "pages": {"current": page, "previous": max(page - 1, 1),
                  "next": max(1, min(page + 1, math.ceil(count / limit)))}

    }
    return render(request, "recipe_manager/index.html", context)


@login_required(login_url='/accounts/login/')
def recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    selected_recipe = Recipe.objects.filter(id=recipe_id, owner=uid).first()
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
    Recipe.objects.filter(id=recipe_id, owner=uid).first().delete()
    return redirect(index)


@login_required(login_url='/accounts/login/')
def execute_recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    template_recipe = Recipe.objects.filter(id=recipe_id, owner=uid).first()
    batch = template_recipe.create_batch()
    batch.name = "Batch " + str(batch.id)
    batch.save()
    return redirect("/batches/batch/" + str(batch.id))


@login_required(login_url='/accounts/login/')
def import_recipe(request):
    imported_recipe = Recipe.objects.create(owner=request.user)
    try:
        recipe_json = json.loads(request.POST.get('jsondata', ''))
        [setattr(imported_recipe, x, recipe_json["fields"][x]) for x in recipe_json["fields"].keys()]
        for p in recipe_json["processes"]:
            imported_process = Process.objects.create(owner=request.user, related_recipe=imported_recipe)
            for x in p["fields"].keys():
                if parse_duration(p["fields"][x]) is not None:
                    setattr(imported_process, x, parse_duration(p["fields"][x]))
                else:
                    setattr(imported_process, x, p["fields"][x])
            if "ingredients" in p:
                for ingredient in p["ingredients"]:
                    amount = float(ingredient["fields"]["amount"])
                    unit = ingredient["fields"]["unit"]
                    name = ingredient["fields"]["name"]
                    imported_ingredient = RecipeIngredient.objects.create(owner=request.user,
                                                                          related_process=imported_process,
                                                                          amount=amount, unit=unit, name=name)
                    imported_ingredient.save()
            if "utensils" in p:
                for utensil in p["utensils"]:
                    name = utensil["fields"]["name"]
                    imported_utensil = Utensils.objects.create(owner=request.user, related_process=imported_process,
                                                               name=name)
                    imported_utensil.save()
            if "process_steps" in p:
                for ps in p["process_steps"]:
                    text = ps["fields"]["text"]
                    process_step_index = ps["fields"]["index"]
                    imported_ps = ProcessStep.objects.create(owner=request.user, related_process=imported_process,
                                                             text=text, index=int(process_step_index))
                    imported_ps.save()
            if "process_schedules" in p:
                for schedule in p["process_schedules"]:
                    executed_once = schedule["fields"]["executed_once"]
                    start_time = parse_duration(schedule["fields"]["start_time"])
                    end_time = parse_duration(schedule["fields"]["end_time"])
                    wait_time = parse_duration(schedule["fields"]["wait_time"])
                    imported_schedule = ProcessSchedule.objects.create(owner=request.user,
                                                                       related_process=imported_process,
                                                                       executed_once=executed_once,
                                                                       start_time=start_time, end_time=end_time,
                                                                       wait_time=wait_time)
                    imported_schedule.save()

            imported_process.save()
        imported_recipe.save()
    except:
        imported_recipe.delete()
        request.session["error"] = "Could not parse recipe!"
        return redirect(request.path.replace("/import", "/#modal-2"))

    return redirect("/recipe_manager/recipe/" + str(imported_recipe.id))


@login_required(login_url='/accounts/login/')
def export_recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    template_recipe = Recipe.objects.filter(id=recipe_id, owner=uid).first()
    js = json.loads(serializers.serialize('json', [template_recipe, ]))[0]
    del js["pk"]
    del js["model"]
    del js["fields"]["owner"]
    del js["fields"]["image"]
    del js["fields"]["cropping"]
    js["processes"] = []
    for process in template_recipe.get_processes():
        js_process = json.loads(serializers.serialize('json', [process, ]))[0]
        del js_process["pk"]
        del js_process["model"]
        del js_process["fields"]["owner"]
        del js_process["fields"]["related_recipe"]

        js_process["ingredients"] = []
        for ingredient in process.get_ingredients():
            js_ingredient = json.loads(serializers.serialize('json', [ingredient, ]))[0]
            del js_ingredient["pk"]
            del js_ingredient["model"]
            del js_ingredient["fields"]["owner"]
            del js_ingredient["fields"]["related_process"]
            js_process["ingredients"].append(js_ingredient)

        js_process["utensils"] = []
        for utensil in process.get_utensils():
            js_utensil = json.loads(serializers.serialize('json', [utensil, ]))[0]
            del js_utensil["pk"]
            del js_utensil["model"]
            del js_utensil["fields"]["owner"]
            del js_utensil["fields"]["related_process"]
            js_process["utensils"].append(js_utensil)

        js_process["process_steps"] = []
        for process_step in process.get_process_steps():
            js_process_step = json.loads(serializers.serialize('json', [process_step, ]))[0]
            del js_process_step["pk"]
            del js_process_step["model"]
            del js_process_step["fields"]["owner"]
            del js_process_step["fields"]["related_process"]
            js_process["process_steps"].append(js_process_step)

        js_process["process_schedules"] = []
        for process_schedule in process.get_process_schedule():
            js_process_schedule = json.loads(serializers.serialize('json', [process_schedule, ]))[0]
            del js_process_schedule["pk"]
            del js_process_schedule["model"]
            del js_process_schedule["fields"]["owner"]
            del js_process_schedule["fields"]["related_process"]
            js_process["process_schedules"].append(js_process_schedule)

        js["processes"].append(js_process)

    return HttpResponse(
        json.dumps(js, ensure_ascii=False),
        content_type='application/force-download'
    )


@login_required(login_url='/accounts/login/')
def edit_recipe_by_id(request, recipe_id):
    if request.method == "GET":
        return edit_recipe_get(request, recipe_id)


@login_required(login_url='/accounts/login/')
def edit_recipe_get(request, recipe_id):
    uid = request.session['_auth_user_id']
    selected_recipe = Recipe.objects.filter(id=recipe_id, owner=uid).first()
    template = loader.get_template("recipe_manager/components/create_recipe.html")
    processes = json.loads(serializers.serialize('json', selected_recipe.get_processes()))
    for i, p in enumerate(processes):
        processes[i]["ingredients"] = json.loads(serializers.serialize('json',
                                                                       RecipeIngredient.objects.filter(
                                                                           related_process=p["pk"])))
        processes[i]["process_steps"] = json.loads(serializers.serialize('json', ProcessStep.objects.filter(
            related_process=p["pk"]).order_by("index")))
        processes[i]["utils"] = json.loads(
            serializers.serialize('json', Utensils.objects.filter(related_process=p["pk"])))
        processes[i]["schedule"] = json.loads(serializers.serialize('json',
                                                                    ProcessSchedule.objects.filter(
                                                                        related_process=p["pk"])))
    recipe_json = json.loads(serializers.serialize('json', [selected_recipe, ]))[0]
    recipe_json["processes"] = processes
    recipe_json = json.dumps(recipe_json, ensure_ascii=False)
    context = {
        "recipe": selected_recipe,
        "recipe_json": recipe_json,
        # "process_json": processes
    }
    return HttpResponse(template.render(context, request))


@transaction.atomic
@login_required(login_url='/accounts/login/')
def recipe_save(request):
    p = RecipeParser()
    try:
        recipe = p.parse_recipe(request)
        return JsonResponse({'status': 'success', 'recipe_id': recipe.id})
    except Exception as e:
        return JsonResponse(status=400, data={'status': 'false', 'message': str(e)})


@login_required(login_url='/accounts/login/')
def recipe_create(request):
    if request.method == "GET":
        return recipe_create_get(request)


def recipe_create_get(request):
    template = loader.get_template("recipe_manager/components/create_recipe.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


def not_found(request, e):
    print(e)
    return render(request, "recipe_manager/recipe_notfound_error.html")


def _input_to_timedelta(input_string):
    total_seconds = 0
    if str(input_string).isdigit():
        total_seconds += int(input_string) * 24 * 60 * 60
        return total_seconds
    if len(input_string.split(" ")) > 1:
        days = input_string.split(" ")[0]
        time = input_string.split(" ")[1]
        total_seconds += (int(days) * 24 * 60 * 60)
    else:
        time = input_string.split(" ")[0]
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1])
    if len(time.split(":")) == 3:
        seconds = int(time.split(":")[2])
    else:
        seconds = 0
    total_seconds += hours * 60 * 60
    total_seconds += minutes * 60
    total_seconds += seconds
    return total_seconds
