from rest_framework import serializers

from .models import Recipe


class RecipeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ["cropping", "image", "owner"]


class RecipePostSerializer(RecipeBaseSerializer):
    class Meta:
        model = Recipe
        exclude = RecipeBaseSerializer.Meta.exclude + ["id"]
