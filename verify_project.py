#!/usr/bin/env python3
"""
Quick verification script to test all components of the Chemical Equipment Visualizer
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print_success(f"{description}: {dirpath}")
        return True
    else:
        print_error(f"{description} not found: {dirpath}")
        return False

def main():
    print_header("Chemical Equipment Visualizer - Verification")
    
    # Get project root
    project_root = Path(__file__).parent
    
    all_checks_passed = True
    
    # ============================================================
    # 1. Check Project Structure
    # ============================================================
    print_header("1. Project Structure")
    
    structure_checks = [
        (project_root / "backend", "Backend directory"),
        (project_root / "frontend-web", "Web frontend directory"),
        (project_root / "desktop", "Desktop frontend directory"),
        (project_root / "assets", "Assets directory"),
        (project_root / "README.md", "README file"),
        (project_root / "DEMO_GUIDE.md", "Demo guide"),
        (project_root / "REQUIREMENTS_CHECKLIST.md", "Requirements checklist"),
    ]
    
    for path, desc in structure_checks:
        if path.is_dir():
            if not check_directory_exists(path, desc):
                all_checks_passed = False
        else:
            if not check_file_exists(path, desc):
                all_checks_passed = False
    
    # ============================================================
    # 2. Check Backend Files
    # ============================================================
    print_header("2. Backend Components")
    
    backend_files = [
        (project_root / "backend/manage.py", "Django manage.py"),
        (project_root / "backend/requirements.txt", "Backend requirements"),
        (project_root / "backend/chemical_equipment/settings.py", "Django settings"),
        (project_root / "backend/chemical_equipment/urls.py", "Main URLs"),
        (project_root / "backend/equipment/models.py", "Dataset model"),
        (project_root / "backend/equipment/views.py", "API views"),
        (project_root / "backend/equipment/serializers.py", "DRF serializers"),
        (project_root / "backend/equipment/utils.py", "Utility functions"),
        (project_root / "backend/db.sqlite3", "SQLite database"),
    ]
    
    for path, desc in backend_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False
    
    # ============================================================
    # 3. Check Frontend Web Files
    # ============================================================
    print_header("3. Web Frontend Components")
    
    web_files = [
        (project_root / "frontend-web/package.json", "Package.json"),
        (project_root / "frontend-web/vite.config.js", "Vite config"),
        (project_root / "frontend-web/src/App.jsx", "Main App component"),
        (project_root / "frontend-web/src/App.css", "App styles"),
        (project_root / "frontend-web/index.html", "HTML template"),
    ]
    
    for path, desc in web_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False
    
    # Check if node_modules exists
    if check_directory_exists(project_root / "frontend-web/node_modules", "Node modules"):
        print_success("NPM dependencies installed")
    else:
        print_warning("Node modules not found - run 'npm install' in frontend-web/")
    
    # ============================================================
    # 4. Check Desktop Frontend Files
    # ============================================================
    print_header("4. Desktop Frontend Components")
    
    desktop_files = [
        (project_root / "desktop/main.py", "Desktop application"),
        (project_root / "desktop/requirements.txt", "Desktop requirements"),
    ]
    
    for path, desc in desktop_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False
    
    # ============================================================
    # 5. Check Sample Data
    # ============================================================
    print_header("5. Sample Data")
    
    sample_csv = project_root / "assets/sample_equipment_data.csv"
    if check_file_exists(sample_csv, "Sample CSV"):
        # Read and verify CSV structure
        try:
            with open(sample_csv, 'r') as f:
                header = f.readline().strip()
                expected_columns = "Equipment Name,Type,Flowrate,Pressure,Temperature"
                if header == expected_columns:
                    print_success("CSV has correct column structure")
                else:
                    print_error(f"CSV columns mismatch. Expected: {expected_columns}")
                    all_checks_passed = False
                
                # Count data rows
                data_rows = len(f.readlines())
                print_success(f"CSV contains {data_rows} data rows")
        except Exception as e:
            print_error(f"Error reading CSV: {e}")
            all_checks_passed = False
    else:
        all_checks_passed = False
    
    # ============================================================
    # 6. Check Backend Dependencies
    # ============================================================
    print_header("6. Backend Dependencies")
    
    backend_venv = project_root / "backend/venv"
    if check_directory_exists(backend_venv, "Backend virtual environment"):
        print_success("Backend venv exists")
        
        # Check if key packages are in requirements
        req_file = project_root / "backend/requirements.txt"
        with open(req_file, 'r') as f:
            requirements = f.read()
            required_packages = ['Django', 'djangorestframework', 'pandas', 'reportlab', 'django-cors-headers']
            for pkg in required_packages:
                if pkg.lower() in requirements.lower():
                    print_success(f"Required package: {pkg}")
                else:
                    print_error(f"Missing package: {pkg}")
                    all_checks_passed = False
    else:
        print_warning("Backend venv not found - run 'python3 -m venv venv' in backend/")
    
    # ============================================================
    # 7. Check API Endpoints Configuration
    # ============================================================
    print_header("7. API Configuration")
    
    urls_file = project_root / "backend/equipment/urls.py"
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            urls_content = f.read()
            endpoints = ['upload/', 'history/', 'report/']
            for endpoint in endpoints:
                if endpoint in urls_content:
                    print_success(f"API endpoint configured: {endpoint}")
                else:
                    print_error(f"Missing endpoint: {endpoint}")
                    all_checks_passed = False
    
    # ============================================================
    # 8. Check Authentication
    # ============================================================
    print_header("8. Authentication Setup")
    
    settings_file = project_root / "backend/chemical_equipment/settings.py"
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings_content = f.read()
            if 'BasicAuthentication' in settings_content:
                print_success("HTTP Basic Authentication configured")
            else:
                print_error("Basic Authentication not found in settings")
                all_checks_passed = False
            
            if 'IsAuthenticated' in settings_content:
                print_success("Authentication required for API")
            else:
                print_error("Authentication permission not configured")
                all_checks_passed = False
    
    # ============================================================
    # 9. Check Deployment Configuration
    # ============================================================
    print_header("9. Deployment Configuration")
    
    deployment_files = [
        (project_root / "Procfile", "Procfile (Railway)"),
        (project_root / "railway.json", "Railway config"),
        (project_root / "render.yaml", "Render config"),
        (project_root / "frontend-web/vercel.json", "Vercel config"),
    ]
    
    for path, desc in deployment_files:
        check_file_exists(path, desc)
    
    # ============================================================
    # 10. Final Summary
    # ============================================================
    print_header("Verification Summary")
    
    if all_checks_passed:
        print_success("ALL CHECKS PASSED! ✨")
        print(f"\n{GREEN}Your application is ready for submission!{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("1. Record demo video (2-3 minutes)")
        print("2. Push to GitHub (if not already done)")
        print("3. Submit via: https://forms.gle/rEgLy6fQU1UgdB5LA")
    else:
        print_warning("Some checks failed. Please review the errors above.")
        print(f"\n{YELLOW}Fix the issues and run this script again.{RESET}")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
