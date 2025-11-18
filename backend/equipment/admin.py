from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = (
        'original_filename',
        'uploaded_at',
        'total_records',
        'avg_flowrate',
        'avg_pressure',
        'avg_temperature',
    )
    readonly_fields = ('uploaded_at',)
    search_fields = ('original_filename',)
