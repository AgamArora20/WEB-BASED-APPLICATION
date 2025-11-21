# Chemical Equipment Parameter Visualizer - Demo Guide

## 📋 Project Overview

This is a **Hybrid Web + Desktop Application** that provides data visualization and analytics for chemical equipment. The application features:

- **Backend**: Django + Django REST Framework (Python)
- **Web Frontend**: React.js + Vite + Chart.js
- **Desktop Frontend**: PyQt5 + Matplotlib
- **Database**: SQLite (development) / PostgreSQL (production)
- **Data Processing**: Pandas
- **PDF Generation**: ReportLab

## 🎯 Key Features Implemented

✅ **CSV Upload** - Both web and desktop clients can upload CSV files  
✅ **Data Summary API** - Returns total count, averages, and equipment type distribution  
✅ **Visualization** - Chart.js (web) and Matplotlib (desktop) for charts  
✅ **History Management** - Stores last 5 uploaded datasets  
✅ **PDF Report Generation** - Automatic PDF reports for each upload  
✅ **Basic Authentication** - HTTP Basic Auth for API security  
✅ **Sample Data** - Included `sample_equipment_data.csv` for testing  

## 🚀 Quick Start Guide

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/backend"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for authentication
python manage.py createsuperuser
# Username: agamarora
# Password: 12345678

# Start the development server
python manage.py runserver 0.0.0.0:8000
```

The backend will be available at: `http://127.0.0.1:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to frontend directory
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/frontend-web"

# Install dependencies
npm install

# Start the development server
npm run dev
```

The web app will be available at: `http://localhost:5173`

### 3. Desktop Frontend Setup (PyQt5)

```bash
# Navigate to desktop directory
cd "/Users/agamarora/Desktop/WEB-BASED APPLICATION/desktop"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the desktop application
python main.py
```

## 📊 Demo Workflow

### Using the Web Application

1. **Open the web app** at `http://localhost:5173`
2. **Enter credentials** in the header:
   - Username: `agamarora`
   - Password: `12345678`
3. **Upload CSV file**:
   - Click "Choose File"
   - Select `assets/sample_equipment_data.csv`
   - Click "Upload & Analyze"
4. **View Results**:
   - Latest Summary section shows KPIs (Total Equipment, Avg Flowrate, Avg Pressure, Avg Temperature)
   - Pie chart displays equipment type distribution
   - Upload History table shows last 5 uploads
5. **Download PDF Report**:
   - Click "PDF" link in the history table

### Using the Desktop Application

1. **Launch the desktop app**: `python main.py`
2. **Configure Connection**:
   - API Base URL: `http://127.0.0.1:8000/api`
   - Username: `agamarora`
   - Password: `12345678`
3. **Upload CSV**:
   - Click "Browse..." to select a file
   - OR click "Use Sample CSV" to use the bundled sample
   - Click "Upload & Analyze"
4. **View Results**:
   - Summary metrics displayed in the right panel
   - Matplotlib pie chart shows equipment type distribution
   - History table shows recent uploads
5. **Open PDF Report**:
   - Select a row in the history table
   - Click "Open Selected Report"

## 🔌 API Endpoints

All endpoints require HTTP Basic Authentication.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload/` | Upload CSV file (multipart/form-data with `file` field) |
| `GET` | `/api/history/` | Get last 5 dataset summaries |
| `GET` | `/api/datasets/<uuid>/report/` | Download PDF report for a specific dataset |

### Example API Usage

```bash
# Upload a CSV file
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -u agamarora:12345678 \
  -F "file=@assets/sample_equipment_data.csv"

# Get upload history
curl -X GET http://127.0.0.1:8000/api/history/ \
  -u agamarora:12345678

# Download PDF report
curl -X GET http://127.0.0.1:8000/api/datasets/<uuid>/report/ \
  -u agamarora:12345678 \
  --output report.pdf
```

## 📁 Sample CSV Format

The CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120,30,80
Valve B,Valve,100,25,75
Reactor C,Reactor,200,40,150
```

**Required Columns**:
- Equipment Name (string)
- Type (string)
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

## 🌐 Live Deployment

- **Web Application**: [https://frontend-m1zq4qarg-agam-aroras-projects-98ceac60.vercel.app](https://frontend-m1zq4qarg-agam-aroras-projects-98ceac60.vercel.app)
- **Backend API**: [https://web-production-68d9f.up.railway.app](https://web-production-68d9f.up.railway.app)
- **Credentials**: 
  - Username: `agamarora`
  - Password: `12345678`

## 🎥 Demo Video Script (2-3 minutes)

### Introduction (15 seconds)
"Hello! I'm demonstrating the Chemical Equipment Parameter Visualizer, a hybrid web and desktop application built with Django, React, and PyQt5."

### Backend Overview (20 seconds)
"The backend is powered by Django REST Framework, providing three main API endpoints: upload, history, and report generation. All endpoints are secured with HTTP Basic Authentication."

### Web Application Demo (45 seconds)
1. "Let's start with the web application built with React and Vite."
2. "First, I'll enter my credentials in the header."
3. "Now I'll upload the sample CSV file containing chemical equipment data."
4. "The application immediately processes the data and displays key metrics: total equipment count, average flowrate, pressure, and temperature."
5. "The pie chart visualizes the equipment type distribution using Chart.js."
6. "The history table shows the last 5 uploads, and I can download the auto-generated PDF report."

### Desktop Application Demo (45 seconds)
1. "Now let's look at the PyQt5 desktop application."
2. "I'll configure the API connection with the same credentials."
3. "I can either browse for a CSV file or use the bundled sample data."
4. "After uploading, the desktop app displays the same metrics and visualizations."
5. "The Matplotlib chart renders the equipment type distribution."
6. "I can select any upload from the history and open its PDF report directly."

### Technical Highlights (20 seconds)
"Key technical features include:
- Pandas for CSV processing and analytics
- ReportLab for PDF generation
- CORS configuration for cross-origin requests
- Automatic history management (last 5 datasets)
- Shared authentication between web and desktop clients"

### Conclusion (15 seconds)
"This hybrid application demonstrates full-stack development with a unified backend serving both web and desktop frontends. Thank you for watching!"

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Build Test
```bash
cd frontend-web
npm run build
```

### Desktop Smoke Test
```bash
cd desktop
python main.py
```

## 📦 Deployment Options

### Option 1: Render (Full Stack)
- Uses `render.yaml` blueprint
- Provisions Django backend, React frontend, and PostgreSQL database
- See README.md for detailed instructions

### Option 2: Railway (Backend) + Vercel (Frontend)
- Backend on Railway (free tier)
- Frontend on Vercel
- Uses `Procfile` and `railway.json`
- See README.md for detailed instructions

## 🔧 Environment Variables

### Backend
- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Debug mode (True/False)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DJANGO_CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of CORS origins
- `DATABASE_URL`: Database connection URL (optional, defaults to SQLite)

### Frontend
- `VITE_API_BASE_URL`: Backend API base URL (e.g., `http://127.0.0.1:8000/api`)

## 📝 Project Structure

```
WEB-BASED APPLICATION/
├── backend/                    # Django backend
│   ├── chemical_equipment/     # Main Django project
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # URL routing
│   │   └── views.py            # Root API view
│   ├── equipment/              # Equipment app
│   │   ├── models.py           # Dataset model
│   │   ├── views.py            # API views
│   │   ├── serializers.py      # DRF serializers
│   │   ├── urls.py             # App URLs
│   │   └── utils.py            # Data processing & PDF generation
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
├── frontend-web/               # React web frontend
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Styles
│   │   └── main.jsx            # Entry point
│   ├── package.json            # NPM dependencies
│   └── vite.config.js          # Vite configuration
├── desktop/                    # PyQt5 desktop frontend
│   ├── main.py                 # Desktop application
│   └── requirements.txt        # Python dependencies
├── assets/                     # Sample data
│   └── sample_equipment_data.csv
└── README.md                   # Project documentation
```

## 🎓 Learning Outcomes

This project demonstrates:
- **Full-stack development** with Django REST Framework
- **Frontend frameworks** (React with Vite)
- **Desktop GUI development** with PyQt5
- **Data visualization** with Chart.js and Matplotlib
- **API design** and RESTful principles
- **Authentication** and security
- **File handling** and CSV processing
- **PDF generation** with ReportLab
- **Deployment** to cloud platforms
- **Version control** with Git

## 📞 Support

For issues or questions:
1. Check the README.md for detailed setup instructions
2. Review the API documentation
3. Verify environment variables are correctly set
4. Ensure all dependencies are installed

## 🏆 Submission Checklist

- ✅ Source code on GitHub
- ✅ README with setup instructions
- ✅ Demo video (2-3 minutes)
- ✅ Live deployment link (optional)
- ✅ All required features implemented
- ✅ Sample CSV data included
- ✅ Both web and desktop frontends working
- ✅ PDF report generation functional
- ✅ Authentication implemented
- ✅ History management (last 5 datasets)

---

**Good luck with your intern screening task!** 🚀
