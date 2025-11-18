from __future__ import annotations

import os
import sys
from typing import List, Dict, Any

import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets, QtGui

ASSETS_SAMPLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'sample_equipment_data.csv'))
DEFAULT_API_BASE = 'http://127.0.0.1:8000/api'


class PieChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(4, 4))
        super().__init__(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.setParent(parent)
        self.figure.tight_layout()

    def plot_distribution(self, distribution: Dict[str, Any]):
        self.axes.clear()
        if not distribution:
            self.axes.text(0.5, 0.5, 'No type data', ha='center', va='center')
        else:
            labels = list(distribution.keys())
            values = list(distribution.values())
            self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        self.draw_idle()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.resize(1100, 720)
        self.datasets: List[Dict[str, Any]] = []
        self.selected_file_path: str | None = None

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        layout.addLayout(self._build_connection_row())
        layout.addWidget(self._build_upload_group())

        content_split = QtWidgets.QSplitter()
        content_split.setOrientation(QtCore.Qt.Horizontal)
        layout.addWidget(content_split, 1)

        content_split.addWidget(self._build_history_table())
        content_split.addWidget(self._build_chart_panel())

        self.statusBar().showMessage('Enter credentials and click "Refresh" to load history.')

    def _build_connection_row(self):
        row = QtWidgets.QHBoxLayout()
        self.api_input = QtWidgets.QLineEdit(DEFAULT_API_BASE)
        self.api_input.setPlaceholderText('API Base URL (e.g. http://127.0.0.1:8000/api)')
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        refresh_button = QtWidgets.QPushButton('Refresh History')
        refresh_button.clicked.connect(self.fetch_history)

        row.addWidget(QtWidgets.QLabel('API'))
        row.addWidget(self.api_input, 1)
        row.addWidget(QtWidgets.QLabel('Username'))
        row.addWidget(self.username_input)
        row.addWidget(QtWidgets.QLabel('Password'))
        row.addWidget(self.password_input)
        row.addWidget(refresh_button)
        return row

    def _build_upload_group(self):
        group = QtWidgets.QGroupBox('Upload CSV')
        layout = QtWidgets.QHBoxLayout(group)

        self.file_label = QtWidgets.QLabel('No file selected')
        pick_button = QtWidgets.QPushButton('Choose CSV')
        pick_button.clicked.connect(self.select_file)

        sample_button = QtWidgets.QPushButton('Use Sample CSV')
        sample_button.clicked.connect(self.use_sample_file)

        upload_button = QtWidgets.QPushButton('Upload & Analyze')
        upload_button.clicked.connect(self.upload_file)

        layout.addWidget(self.file_label, 1)
        layout.addWidget(pick_button)
        layout.addWidget(sample_button)
        layout.addWidget(upload_button)
        return group

    def _build_history_table(self):
        container = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(container)
        self.history_table = QtWidgets.QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            'Filename', 'Uploaded', 'Total', 'Flowrate', 'Pressure', 'Temperature', 'Report'
        ])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.history_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.history_table.itemSelectionChanged.connect(self._selection_changed)

        self.open_report_button = QtWidgets.QPushButton('Open Selected Report')
        self.open_report_button.setEnabled(False)
        self.open_report_button.clicked.connect(self.open_selected_report)

        vbox.addWidget(QtWidgets.QLabel('History (last 5 uploads)'))
        vbox.addWidget(self.history_table, 1)
        vbox.addWidget(self.open_report_button)
        return container

    def _build_chart_panel(self):
        container = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(container)
        self.summary_labels = {
            'total': QtWidgets.QLabel('Total Equipment: —'),
            'flow': QtWidgets.QLabel('Avg Flowrate: —'),
            'pressure': QtWidgets.QLabel('Avg Pressure: —'),
            'temperature': QtWidgets.QLabel('Avg Temperature: —'),
        }
        for label in self.summary_labels.values():
            label.setStyleSheet('font-size: 16px;')
            vbox.addWidget(label)
        self.chart = PieChartCanvas(container)
        vbox.addWidget(self.chart, 1)
        return container

    # UI callbacks
    def select_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select CSV file', '', 'CSV Files (*.csv)')
        if path:
            self.selected_file_path = path
            self.file_label.setText(os.path.basename(path))

    def use_sample_file(self):
        self.selected_file_path = ASSETS_SAMPLE
        self.file_label.setText(os.path.basename(ASSETS_SAMPLE))

    def upload_file(self):
        if not self.selected_file_path:
            self._show_message('Choose a CSV file first.')
            return
        try:
            with open(self.selected_file_path, 'rb') as file_handle:
                files = {'file': file_handle}
                response = requests.post(
                    self._url('upload/'),
                    files=files,
                    auth=self._auth(),
                    timeout=30,
                )
            response.raise_for_status()
            self._show_message('Upload successful. History updated.', success=True)
            self.fetch_history()
        except Exception as exc:  # pragma: no cover - user feedback
            self._show_message(f'Upload failed: {exc}')

    def fetch_history(self):
        try:
            response = requests.get(self._url('history/'), auth=self._auth(), timeout=30)
            response.raise_for_status()
            self.datasets = response.json()
            self._populate_table()
            if self.datasets:
                self._update_summary(self.datasets[0])
            else:
                self._update_summary(None)
        except Exception as exc:  # pragma: no cover - user feedback
            self._show_message(f'Unable to fetch history: {exc}')

    def open_selected_report(self):
        row = self.history_table.currentRow()
        if row < 0:
            return
        dataset = self.datasets[row]
        pdf_path = dataset.get('summary_pdf')
        if not pdf_path:
            self._show_message('Selected dataset has no PDF yet.')
            return
        full_url = self._root_url() + pdf_path
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(full_url))

    # Helpers
    def _populate_table(self):
        self.history_table.setRowCount(len(self.datasets))
        for row, dataset in enumerate(self.datasets):
            values = [
                dataset.get('original_filename', ''),
                dataset.get('uploaded_at', ''),
                str(dataset.get('total_records', '')),
                self._format_metric(dataset.get('avg_flowrate')),
                self._format_metric(dataset.get('avg_pressure')),
                self._format_metric(dataset.get('avg_temperature')),
                'Available' if dataset.get('summary_pdf') else 'Pending',
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                self.history_table.setItem(row, col, item)
        self.open_report_button.setEnabled(bool(self.datasets))

    def _format_metric(self, value):
        return '—' if value is None else f'{value}'

    def _update_summary(self, dataset: Dict[str, Any] | None):
        if not dataset:
            for label in self.summary_labels.values():
                label.setText(label.text().split(':')[0] + ': —')
            self.chart.plot_distribution({})
            return
        self.summary_labels['total'].setText(f"Total Equipment: {dataset.get('total_records', '—')}")
        self.summary_labels['flow'].setText(f"Avg Flowrate: {self._format_metric(dataset.get('avg_flowrate'))}")
        self.summary_labels['pressure'].setText(f"Avg Pressure: {self._format_metric(dataset.get('avg_pressure'))}")
        self.summary_labels['temperature'].setText(f"Avg Temperature: {self._format_metric(dataset.get('avg_temperature'))}")
        self.chart.plot_distribution(dataset.get('type_distribution', {}))

    def _selection_changed(self):
        row = self.history_table.currentRow()
        self.open_report_button.setEnabled(row >= 0 and bool(self.datasets[row].get('summary_pdf')))

    def _url(self, path: str):
        base = self.api_input.text().rstrip('/')
        return f"{base}/{path}"

    def _root_url(self):
        base = self.api_input.text().rstrip('/')
        if base.endswith('/api'):
            base = base[:-4]
        return base

    def _auth(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            raise ValueError('Username and password are required')
        return (username, password)

    def _show_message(self, text: str, success: bool = False):
        self.statusBar().showMessage(text, 5000)
        if success:
            QtWidgets.QMessageBox.information(self, 'Success', text)
        else:
            QtWidgets.QMessageBox.warning(self, 'Notice', text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
