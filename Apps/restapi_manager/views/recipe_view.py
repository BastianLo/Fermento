from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from Apps.recipe_manager.models import recipe
from rest_framework import generics

from Apps.recipe_manager.serializers import RecipeBaseSerializer


@permission_classes([IsAuthenticated])
class recipeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return recipe.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class RecipeCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeBaseSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return recipe.objects.filter(owner=user)