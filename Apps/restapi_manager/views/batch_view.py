from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.batches.models import Batch, QrCode, Execution, JournalEntry
from Apps.batches.serializers import BatchBaseSerializer, BatchPostSerializer, QrCodeBaseSerializer, \
    QrCodePostSerializer, ExecutionBaseSerializer, ExecutionPostSerializer, JournalEntryBaseSerializer, \
    JournalEntryPostSerializer


@permission_classes([IsAuthenticated])
class BatchDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BatchBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Batch.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class BatchListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["id", "name", "description", "start_date", "related_recipe"]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BatchBaseSerializer
        return BatchPostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Batch.objects.filter(owner=user)


@permission_classes([IsAuthenticated])
class QrCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QrCodeBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return QrCode.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class QrCodeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        "name": ["exact"],
        "description": ["exact"],
        "batch": ["exact", "isnull"],
        "id": ["exact"],
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QrCodeBaseSerializer
        return QrCodePostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return QrCode.objects.filter(owner=user)


@permission_classes([IsAuthenticated])
class ExecutionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExecutionBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Execution.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class ExecutionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExecutionBaseSerializer
        return ExecutionPostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Execution.objects.filter(owner=user)


@permission_classes([IsAuthenticated])
class JournalEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntryBaseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return JournalEntry.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class JournalEntryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["created_datetime", "related_batch", "title", "description"]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JournalEntryBaseSerializer
        return JournalEntryPostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return JournalEntry.objects.filter(owner=user)
