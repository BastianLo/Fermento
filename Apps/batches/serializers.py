from rest_framework import serializers

from .models import Batch


### Batch ###
class BatchBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        exclude = ["owner"]


class BatchPostSerializer(BatchBaseSerializer):
    class Meta:
        model = Batch
        exclude = BatchBaseSerializer.Meta.exclude + ["id"]
