from rest_framework import serializers

from .models import Batch, QrCode, Execution


### Batch ###
class BatchBaseSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField(source='get_progress_percentage')
    end_date = serializers.DateTimeField(read_only=True, source='get_end_date')

    class Meta:
        model = Batch
        exclude = ["owner"]


class BatchPostSerializer(BatchBaseSerializer):
    class Meta:
        model = Batch
        exclude = BatchBaseSerializer.Meta.exclude + ["id"]


### QrCode ###
class QrCodeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        exclude = ["owner"]


class QrCodePostSerializer(QrCodeBaseSerializer):
    class Meta:
        model = QrCode
        exclude = QrCodeBaseSerializer.Meta.exclude + ["id"]


### Execution ###
class ExecutionBaseSerializer(serializers.ModelSerializer):
    overdue = serializers.ReadOnlyField(source='is_overdue')

    class Meta:
        model = Execution
        exclude = ["owner"]


class ExecutionPostSerializer(ExecutionBaseSerializer):
    class Meta:
        model = Execution
        exclude = ExecutionBaseSerializer.Meta.exclude + ["id"]
