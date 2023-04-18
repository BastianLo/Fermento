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
from django.core import serializers
from django.utils.dateparse import parse_duration
import math

@login_required(login_url='/accounts/login/')
def index(request):
    LIMIT = 10
    recipes = recipe.objects.filter(owner=request.user)
    count = len(recipes)
    orderby = request.GET.get("orderby")
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    if orderby:
        try:
            desc = "-" if request.GET.get("direction") == "desc" else ""
            recipes = recipes.order_by(desc + orderby)
        except:
            print(f"Error: '{orderby}' attribute does not exist for object Batch")
    recipes = recipes[(page-1)*LIMIT:(page-1)*LIMIT+LIMIT]
    context = {
        "recipes": recipes,
        "order_items": ["name", "difficulty"],
        "order_directions": ["asc", "desc"],
        "pages": {"current": page, "previous": max(page-1, 1), "next": max(1,min(page+1, math.ceil(count/LIMIT)))}

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
def execute_recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    template_recipe = recipe.objects.filter(id=recipe_id, owner=uid).first()
    batch = template_recipe.create_batch()
    batch.name = "Batch " + str(batch.id)
    batch.save()
    return redirect("/batches/batch/" + str(batch.id))



@login_required(login_url='/accounts/login/')
def import_recipe(request):
    imported_recipe = recipe.objects.create(owner=request.user)
    try:
        recipe_json = json.loads(request.POST.get('jsondata', ''))
        [setattr(imported_recipe, x, recipe_json["fields"][x]) for x in  recipe_json["fields"].keys()]
        for p in recipe_json["processes"]:
            imported_process = process.objects.create(owner=request.user, related_recipe=imported_recipe)
            for x in p["fields"].keys():
                if parse_duration(p["fields"][x]) != None:
                    setattr(imported_process, x, parse_duration(p["fields"][x]))
                else:
                    setattr(imported_process, x, p["fields"][x])
            if "ingredients" in  p:
                for ingr in p["ingredients"]:
                    amount = float(ingr["fields"]["amount"])
                    unit = ingr["fields"]["unit"]
                    name = ingr["fields"]["name"]
                    imported_ingredient = recipe_ingredient.objects.create(owner=request.user, related_process=imported_process, amount=amount, unit=unit, name=name)
                    imported_ingredient.save()
            if "utensils" in p:
                for utens in p["utensils"]:
                    name = utens["fields"]["name"]
                    imported_utensil = utensils.objects.create(owner=request.user, related_process=imported_process, name=name)
                    imported_utensil.save()
            if "process_steps" in p:
                for ps in p["process_steps"]:
                    text = ps["fields"]["text"]
                    index = ps["fields"]["index"]
                    imported_ps = process_step.objects.create(owner=request.user, related_process=imported_process, text=text, index=int(index))
                    imported_ps.save()
            if "process_schedules" in p:
                for schedule in p["process_schedules"]:
                    executed_once = schedule["fields"]["executed_once"]
                    start_time = parse_duration(schedule["fields"]["start_time"])
                    end_time = parse_duration(schedule["fields"]["end_time"])
                    wait_time = parse_duration(schedule["fields"]["wait_time"])
                    imported_schedule = process_schedule.objects.create(owner=request.user, related_process=imported_process, executed_once=executed_once, start_time=start_time, end_time=end_time, wait_time=wait_time)
                    imported_schedule.save()

            imported_process.save()
        imported_recipe.save()
    except:
        imported_recipe.delete()
        request.session["error"] = "Could not parse recipe!"
        return redirect(request.path.replace("/import", "/#modal-2"))
        #return JsonResponse({'message':'fail','error':True,'code':500,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}})    
    
    return redirect("/recipe_manager/recipe/" + str(imported_recipe.id))

@login_required(login_url='/accounts/login/')
def export_recipe_by_id(request, recipe_id):
    uid = request.session['_auth_user_id']
    template_recipe = recipe.objects.filter(id=recipe_id, owner=uid).first()
    js = json.loads(serializers.serialize('json', [ template_recipe, ]))[0]
    del js["pk"]
    del js["model"]
    del js["fields"]["owner"]
    del js["fields"]["image"]
    del js["fields"]["cropping"]
    js["processes"] = []
    for process in template_recipe.get_processes():
        js_process = json.loads(serializers.serialize('json', [ process, ]))[0]
        del js_process["pk"]
        del js_process["model"]
        del js_process["fields"]["owner"]
        del js_process["fields"]["related_recipe"]

        js_process["ingredients"] = []
        for ingredient in process.get_ingredients():
            js_ingredient = json.loads(serializers.serialize('json', [ ingredient, ]))[0]
            del js_ingredient["pk"]
            del js_ingredient["model"]
            del js_ingredient["fields"]["owner"]
            del js_ingredient["fields"]["related_process"]
            js_process["ingredients"].append(js_ingredient)

        js_process["utensils"] = []
        for utensil in process.get_utensils():
            js_utensil = json.loads(serializers.serialize('json', [ utensil, ]))[0]
            del js_utensil["pk"]
            del js_utensil["model"]
            del js_utensil["fields"]["owner"]
            del js_utensil["fields"]["related_process"]
            js_process["utensils"].append(js_utensil)

        js_process["process_steps"] = []
        for process_step in process.get_process_steps():
            js_process_step = json.loads(serializers.serialize('json', [ process_step, ]))[0]
            del js_process_step["pk"]
            del js_process_step["model"]
            del js_process_step["fields"]["owner"]
            del js_process_step["fields"]["related_process"]
            js_process["process_steps"].append(js_process_step)

        js_process["process_schedules"] = []
        for process_schedule in process.get_process_schedule():
            js_process_schedule = json.loads(serializers.serialize('json', [ process_schedule, ]))[0]
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
    elif request.method == "POST":
        return edit_recipe_post(request, recipe_id)

@login_required(login_url='/accounts/login/')
def edit_recipe_get(request, recipe_id):
    uid = request.session['_auth_user_id']
    selected_recipe = recipe.objects.filter(id=recipe_id, owner=uid).first()
    template = loader.get_template("recipe_manager/components/edit_recipe.html")
    processes = json.loads(serializers.serialize('json', selected_recipe.get_processes()))
    for i, p in enumerate(processes):
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
        new_process.work_duration = parse_duration(p["work_duration"])
        new_process.wait_duration = parse_duration(p["wait_duration"])
        print(new_process.wait_duration)
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
        new_process.work_duration = parse_duration(p["work_duration"])
        new_process.wait_duration = parse_duration(p["wait_duration"])
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

    