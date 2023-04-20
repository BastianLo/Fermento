from rest_framework import serializers
from .models import recipe

class RecipeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = recipe
        exclude = ["cropping", "image", "owner"]

class RecipePostSerializer(RecipeBaseSerializer):
    class Meta:
        model = recipe
        exclude = RecipeBaseSerializer.Meta.exclude + ["id"]