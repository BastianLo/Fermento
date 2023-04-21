from rest_framework import serializers

from .models import Batch, QrCode


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


class QrCodePostSerializer(BatchBaseSerializer):
    class Meta:
        model = QrCode
        exclude = QrCodeBaseSerializer.Meta.exclude + ["id"]
