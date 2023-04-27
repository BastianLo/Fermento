from rest_framework import serializers

from .models import Batch, QrCode, Execution, JournalEntry


### Batch ###
class BatchBaseSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField(source='get_progress_percentage')
    end_date = serializers.DateTimeField(read_only=True, source='get_end_date')
    jar_name = serializers.ReadOnlyField(source='get_jar_name')

    class Meta:
        model = Batch
        exclude = ["owner"]


class BatchPostSerializer(BatchBaseSerializer):
    class Meta:
        model = Batch
        exclude = BatchBaseSerializer.Meta.exclude + ["id"]


### QrCode ###
class QrCodeBaseSerializer(serializers.ModelSerializer):
    batch_name = serializers.ReadOnlyField(source='get_batch_name')

    class Meta:
        model = QrCode
        exclude = ["owner"]


class QrCodePostSerializer(QrCodeBaseSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = QrCode
        exclude = QrCodeBaseSerializer.Meta.exclude


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


### JournalEntry ###
class JournalEntryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        exclude = ["owner"]


class JournalEntryPostSerializer(JournalEntryBaseSerializer):
    class Meta:
        model = JournalEntry
        exclude = ExecutionBaseSerializer.Meta.exclude + ["id"]
