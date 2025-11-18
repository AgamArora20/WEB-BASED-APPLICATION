from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Dict, Any

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

NUMERIC_COLUMNS = {
    'flowrate': 'avg_flowrate',
    'pressure': 'avg_pressure',
    'temperature': 'avg_temperature',
}


def normalize_dataframe(file_like) -> pd.DataFrame:
    df = pd.read_csv(file_like)
    df.columns = [col.strip() for col in df.columns]
    rename_map = {}
    for col in df.columns:
        lower = col.lower()
        if lower in NUMERIC_COLUMNS or lower == 'type' or lower == 'equipment name':
            rename_map[col] = col.title()
    df = df.rename(columns=rename_map)
    return df


def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    summary = {
        'total_records': int(len(df)),
        'avg_flowrate': None,
        'avg_pressure': None,
        'avg_temperature': None,
        'type_distribution': {},
    }

    for column, summary_key in NUMERIC_COLUMNS.items():
        formatted_column = column.title()
        if formatted_column in df.columns:
            numeric_series = pd.to_numeric(df[formatted_column], errors='coerce')
            if not numeric_series.dropna().empty:
                summary[summary_key] = round(float(numeric_series.mean()), 2)

    type_column = next((c for c in df.columns if c.lower() == 'type'), None)
    if type_column:
        distribution = (
            df[type_column]
            .fillna('Unknown')
            .astype(str)
            .str.strip()
            .value_counts()
            .to_dict()
        )
        summary['type_distribution'] = distribution

    return summary


def generate_pdf(summary: Dict[str, Any], dataset_name: str) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin

    c.setFont('Helvetica-Bold', 18)
    c.drawString(margin, y, 'Chemical Equipment Summary Report')
    y -= 30

    c.setFont('Helvetica', 12)
    c.drawString(margin, y, f"Dataset: {dataset_name}")
    y -= 18
    c.drawString(margin, y, f"Generated: {datetime.utcnow():%Y-%m-%d %H:%M UTC}")
    y -= 24

    c.setFont('Helvetica-Bold', 14)
    c.drawString(margin, y, 'Key Metrics')
    y -= 20
    c.setFont('Helvetica', 12)
    metrics = [
        ('Total Records', summary.get('total_records', 0)),
        ('Average Flowrate', summary.get('avg_flowrate', 'N/A')),
        ('Average Pressure', summary.get('avg_pressure', 'N/A')),
        ('Average Temperature', summary.get('avg_temperature', 'N/A')),
    ]

    for label, value in metrics:
        c.drawString(margin + 10, y, f"{label}: {value if value is not None else 'N/A'}")
        y -= 16

    y -= 6
    c.setFont('Helvetica-Bold', 14)
    c.drawString(margin, y, 'Equipment Type Distribution')
    y -= 20
    c.setFont('Helvetica', 12)
    distribution = summary.get('type_distribution', {})
    if not distribution:
        c.drawString(margin + 10, y, 'No type information available.')
        y -= 16
    else:
        for equipment_type, count in distribution.items():
            c.drawString(margin + 10, y, f"{equipment_type}: {count}")
            y -= 16
            if y < margin:
                c.showPage()
                y = height - margin
                c.setFont('Helvetica', 12)

    c.save()
    buffer.seek(0)
    return buffer
