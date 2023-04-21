from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.batches.models import Batch
from Apps.batches.serializers import BatchBaseSerializer, BatchPostSerializer


@permission_classes([IsAuthenticated])
class BatchDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BatchBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Batch.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class BatchListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BatchBaseSerializer
        return BatchPostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Batch.objects.filter(owner=user)
