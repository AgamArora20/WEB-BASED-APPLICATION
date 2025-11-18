# Chemical Equipment Parameter Visualizer

Hybrid analytics platform that shares a single Django REST backend across a React web client and a PyQt5 desktop client. Users can upload chemical equipment CSV files, review computed KPIs, visualize equipment-type distributions, download PDF summaries, and revisit the five most recent datasets.

## Repository Layout

```
backend/        # Django + DRF project (REST API, analytics, PDF generation)
frontend-web/   # Vite + React + Chart.js web dashboard
desktop/        # PyQt5 + Matplotlib desktop dashboard
assets/         # Sample CSV for demos/tests
```

## Key Features

- CSV ingestion with pandas-based validation and analytics
- Summary metrics (total equipment count, averages for flowrate/pressure/temperature)
- Equipment type distribution charts (Chart.js on web, Matplotlib on desktop)
- History limited to the last five uploads (older entries auto-pruned)
- Automatic PDF report generation via ReportLab
- Shared API secured with HTTP Basic Auth (same credentials for web + desktop)

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm

## Backend Setup (Django + DRF)

```bash
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # provides Basic Auth credentials
python manage.py runserver 0.0.0.0:8000
```

Environment defaults:
- API base URL: `http://127.0.0.1:8000/api`
- Media uploads (CSV + PDFs) stored in `backend/media/`

### API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/upload/` | Accepts `multipart/form-data` with a `file` field (CSV). Returns computed summary + dataset metadata. |
| `GET` | `/api/history/` | Returns up to five most recent dataset summaries (ordered newest first). |
| `GET` | `/api/datasets/<uuid>/report/` | Streams the generated PDF report. |

_All endpoints require HTTP Basic Authentication using any Django user account._

## Web Frontend (React + Chart.js)

```bash
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/frontend-web"
cp .env.example .env   # adjust VITE_API_BASE_URL if backend differs
npm install
npm run dev            # launches Vite dev server on http://localhost:5173
```

Enter the same username/password you created on the backend to authenticate API calls. The dashboard supports CSV uploads, KPI cards, pie charts, and download links for generated PDFs.

To build for production: `npm run build`

## Desktop Frontend (PyQt5 + Matplotlib)

```bash
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/desktop"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Features:
- Configure API base URL + credentials at runtime
- Select local CSVs or use the bundled sample at `assets/sample_equipment_data.csv`
- View latest KPIs and charts inside the desktop UI
- Open PDF reports in your default viewer directly from the history table

## Sample Data

`assets/sample_equipment_data.csv` is a ready-to-use dataset that exercises all KPIs and visualization components. Use it for quick demos, automated video walkthroughs, or QA.

## Testing & Verification

- Backend integrity checks: `python manage.py test`
- React compile test: `npm run build`
- Desktop smoke test: `python desktop/main.py` (requires local display environment)

## Deploying to Render

This repository already includes a `render.yaml` blueprint that provisions:

- A Django web service (`chemical-equipment-backend`) served by Gunicorn + Whitenoise
- A static React web service (`chemical-equipment-frontend`) built from Vite
- A managed PostgreSQL instance (`chemical-equipment-db`)

Steps:

1. Push this repository to GitHub.
2. Create a new Render Blueprint instance and point it to the repo.
3. Update the placeholder values inside `render.yaml` (`your-backend.onrender.com`, `your-frontend.onrender.com`) or override them later via the Render dashboard:
   - `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` must include your backend Render URL.
   - `CORS_ALLOWED_ORIGINS` and `VITE_API_BASE_URL` must reference the deployed frontend/backend URLs respectively.
4. Render automatically runs `pip install -r requirements.txt && python manage.py collectstatic --noinput` for the backend and `npm install && npm run build` for the frontend.
5. After the first deploy, run `python manage.py createsuperuser` via the Render shell to configure Basic Auth credentials.

## Demo & Submission Notes

1. Record a short (2–3 min) screen capture showing:
   - CSV upload via the web UI
   - Resulting charts and PDF download
   - Desktop client fetching the shared history
2. Push code + README to GitHub.
3. Submit repository link, demo video, and optional deployment URL via the provided Google Form.

## Future Enhancements

- Deploy Django + React via containerized setup
- Add JWT-based authentication + refresh tokens
- Extend analytics (min/max, outliers, trends)
- Persist more than five datasets with pagination + filtering
- Bundle the desktop app with PyInstaller for one-click installs
