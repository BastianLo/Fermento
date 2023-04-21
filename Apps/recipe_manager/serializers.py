from rest_framework import serializers

from .models import Recipe, Process, ProcessStep, ProcessSchedule, RecipeIngredient, Utensils


### Recipe ###
class RecipeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ["cropping", "image", "owner"]


class RecipePostSerializer(RecipeBaseSerializer):
    class Meta:
        model = Recipe
        exclude = RecipeBaseSerializer.Meta.exclude + ["id"]


### Process ###
class ProcessBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ["owner"]


class ProcessPostSerializer(ProcessBaseSerializer):
    class Meta:
        model = Process
        exclude = ProcessBaseSerializer.Meta.exclude + ["id"]


### Process Step ###
class ProcessStepBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        exclude = ["owner"]


class ProcessStepPostSerializer(ProcessStepBaseSerializer):
    class Meta:
        model = ProcessStep
        exclude = ProcessStepBaseSerializer.Meta.exclude + ["id"]


### Process schedule
class ProcessScheduleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessSchedule
        exclude = ["owner"]


class ProcessSchedulePostSerializer(ProcessScheduleBaseSerializer):
    class Meta:
        model = ProcessSchedule
        exclude = ProcessScheduleBaseSerializer.Meta.exclude + ["id"]


### Process Ingredient ###
class RecipeIngredientBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = ["owner"]


class RecipeIngredientPostSerializer(RecipeIngredientBaseSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = ProcessScheduleBaseSerializer.Meta.exclude + ["id"]


### Process Utensils ###
class UtensilsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utensils
        exclude = ["owner"]


class UtensilsPostSerializer(UtensilsBaseSerializer):
    class Meta:
        model = Utensils
        exclude = UtensilsBaseSerializer.Meta.exclude + ["id"]
