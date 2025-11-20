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

## Deploying the Backend to Railway (card-free option)

If you’d rather keep everything on a free tier without adding payment info, deploy the Django API to [Railway](https://railway.app/) and the React build to Vercel/Netlify. This repo now ships with:

- `Procfile`: tells Railway how to start Gunicorn (`web: cd backend && gunicorn chemical_equipment.wsgi:application`)
- `railway.json`: instructs Railway’s Nixpacks builder to `pip install` + `collectstatic` before launching

Steps:

1. Install the Railway CLI (`npm i -g railway`) and run `railway login`.
2. From the repo root run `railway init` → “Deploy from current directory”.
3. Railway will detect `railway.json` and build the backend automatically.
4. In the Railway dashboard, create a Postgres plugin and copy its connection URL into the `DATABASE_URL` variable.
5. Add the other env vars (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS`, `DJANGO_DEBUG=False`).
6. Visit the deployed URL, then run `railway run python backend/manage.py migrate` and `railway run python backend/manage.py createsuperuser`.
7. Host the React frontend on Vercel/Netlify and set `VITE_API_BASE_URL` to the Railway backend URL.
