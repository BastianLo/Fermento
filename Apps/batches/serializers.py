from rest_framework import serializers

from .models import Batch, QrCode, Execution


### Batch ###
class BatchBaseSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Execution
        exclude = ["owner"]


class ExecutionPostSerializer(ExecutionBaseSerializer):
    class Meta:
        model = Execution
        exclude = ExecutionBaseSerializer.Meta.exclude + ["id"]
