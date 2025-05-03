# 🏥 Hospital Appointment System

A Flask-based web application for booking and managing doctor appointments. It supports user authentication, admin doctor management, and region-based search functionality.

---

## 📦 Features

- User registration, login, and logout
- Admin panel to manage doctors by location
- Users can browse hospitals by region
- Book appointments and view/delete existing bookings
- CSV-based data loading with SQLAlchemy ORM

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- pip (Python package installer)

Install dependencies:



For windows

```bash
pip install -r requirements.txt

# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate the environment
venv\Scripts\activate

# Step 3: Set Flask app
set FLASK_APP=app

# Step 4: Initialize the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

#load csv data
flask shell
from app.data_loader import load_all
load_all()

# Step 5: Run the server
flask run


For Mac/OS

pip install -r requirements.txt

# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate the environment
source venv/bin/activate

# Step 3: Set Flask app
export FLASK_APP=app

# Step 4: Initialize the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

#load csv data
flask shell
from app.data_loader import load_all
load_all()

# Step 5: Run the server
flask run

