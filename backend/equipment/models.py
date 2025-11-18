import uuid
from django.db import models


class Dataset(models.Model):
    """
    Stores metadata and summary statistics for an uploaded equipment CSV file.
    Only the five most recent Dataset entries are retained.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    data_file = models.FileField(upload_to='datasets/')
    total_records = models.PositiveIntegerField(default=0)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    type_distribution = models.JSONField(default=dict, blank=True)
    summary_pdf = models.FileField(upload_to='reports/', null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self) -> str:
        return f"{self.original_filename} ({self.uploaded_at:%Y-%m-%d %H:%M})"

    def delete(self, *args, **kwargs):
        storage = self.data_file.storage if self.data_file else None
        pdf_storage = self.summary_pdf.storage if self.summary_pdf else None
        data_file_name = self.data_file.name if self.data_file else None
        pdf_file_name = self.summary_pdf.name if self.summary_pdf else None
        super().delete(*args, **kwargs)
        if storage and data_file_name:
            storage.delete(data_file_name)
        if pdf_storage and pdf_file_name:
            pdf_storage.delete(pdf_file_name)
