# Qundylyq Project Setup Guide

Follow these steps to set up the project on a new computer.

## 1. Prerequisites
- **Python** (version 3.10 or higher) must be installed.

## 2. Setup (Windows)

Open your terminal (PowerShell or Command Prompt) in this folder and run the following commands one by one:

### Step 1: Create Virtual Environment
```bash
python -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python backend/manage.py migrate
```

### Step 5: Create Admin User (Optional)
To access the admin panel, create a superuser:
```bash
python backend/manage.py createsuperuser
```
*(Follow the prompts to set username and password)*

## 3. Run the Server
Whenever you want to start the website, run:

```bash
python backend/manage.py runserver
```

Then open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.
