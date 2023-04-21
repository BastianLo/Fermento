from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.recipe_manager.models import Recipe
from Apps.recipe_manager.serializers import RecipeBaseSerializer, RecipePostSerializer


@permission_classes([IsAuthenticated])
class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Recipe.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class RecipeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeBaseSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(owner=user)
