from rest_framework import serializers

from .models import Recipe, Process, ProcessStep, ProcessSchedule, RecipeIngredient, Utensils


class RecipeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ["cropping", "image", "owner"]


class RecipePostSerializer(RecipeBaseSerializer):
    class Meta:
        model = Recipe
        exclude = RecipeBaseSerializer.Meta.exclude + ["id"]


class ProcessBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ["owner"]


class ProcessPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ProcessBaseSerializer.Meta.exclude + ["id"]


class ProcessStepBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        exclude = []


class ProcessScheduleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessSchedule
        exclude = []


class RecipeIngredientBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = []


class UtensilsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utensils
        exclude = []
