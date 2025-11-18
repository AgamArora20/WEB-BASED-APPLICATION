from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'id',
            'original_filename',
            'uploaded_at',
            'total_records',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
            'summary_pdf',
        ]
        read_only_fields = fields


class UploadResponseSerializer(serializers.Serializer):
    dataset = DatasetSerializer()
    message = serializers.CharField()
