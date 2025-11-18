from django.urls import path

from .views import DatasetHistoryView, DatasetReportView, UploadDatasetView

urlpatterns = [
    path('upload/', UploadDatasetView.as_view(), name='upload-dataset'),
    path('history/', DatasetHistoryView.as_view(), name='dataset-history'),
    path('datasets/<uuid:dataset_id>/report/', DatasetReportView.as_view(), name='dataset-report'),
]
