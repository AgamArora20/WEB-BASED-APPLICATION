from __future__ import annotations

from io import BytesIO

from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset
from .serializers import DatasetSerializer
from .utils import compute_summary, generate_pdf, normalize_dataframe


HISTORY_LIMIT = 5


class UploadDatasetView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response({'detail': 'CSV file is required under the "file" field.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_bytes = uploaded_file.read()
            dataframe = normalize_dataframe(BytesIO(file_bytes))
        except Exception as exc:  # pragma: no cover - defensive
            return Response({'detail': f'Unable to parse CSV: {exc}'}, status=status.HTTP_400_BAD_REQUEST)

        summary = compute_summary(dataframe)

        dataset = Dataset(
            original_filename=uploaded_file.name,
            total_records=summary['total_records'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature'],
            type_distribution=summary['type_distribution'],
        )
        dataset.data_file.save(uploaded_file.name, ContentFile(file_bytes), save=False)

        pdf_buffer = generate_pdf(summary, uploaded_file.name)
        dataset.summary_pdf.save(f"{dataset.id}_summary.pdf", ContentFile(pdf_buffer.read()), save=False)
        dataset.save()

        self._trim_history()

        serializer = DatasetSerializer(dataset)
        return Response({'message': 'CSV processed successfully.', 'dataset': serializer.data}, status=status.HTTP_201_CREATED)

    @staticmethod
    def _trim_history():
        datasets = Dataset.objects.order_by('-uploaded_at')
        if datasets.count() <= HISTORY_LIMIT:
            return
        for extra in datasets[HISTORY_LIMIT:]:
            extra.delete()


class DatasetHistoryView(generics.ListAPIView):
    serializer_class = DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.order_by('-uploaded_at')[:HISTORY_LIMIT]


class DatasetReportView(APIView):
    def get(self, request, dataset_id: str, *args, **kwargs):
        try:
            dataset = Dataset.objects.get(pk=dataset_id)
        except Dataset.DoesNotExist as exc:  # pragma: no cover - defensive
            raise Http404('Dataset not found') from exc

        if not dataset.summary_pdf:
            raise Http404('Report not available yet')
        return FileResponse(dataset.summary_pdf.open('rb'), as_attachment=True, filename=f"{dataset.original_filename}_summary.pdf")
