from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from Apps.recipe_manager.models import Recipe, Process
from Apps.recipe_manager.serializers import RecipeBaseSerializer, RecipePostSerializer, ProcessBaseSerializer, \
    ProcessPostSerializer


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


@permission_classes([IsAuthenticated])
class ProcessListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProcessBaseSerializer
        return ProcessPostSerializer

    def perform_create(self, serializer):
        if serializer.validated_data["related_recipe"].owner != self.request.user:
            raise PermissionDenied("Recipe does not belong to this user!")
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Process.objects.filter(owner=user)


@permission_classes([IsAuthenticated])
class ProcessDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Process.objects.filter(owner=self.request.user)
