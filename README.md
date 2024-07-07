# Stantech
Certainly! Here's how you can structure the README.md file for your Django project, providing a concise setup guide and overview:

---

# E-commerce Data Analysis and Reporting System

## Overview

This Django-based web application provides a platform for analyzing e-commerce product data and generating comprehensive reports. It includes features for data aggregation, user authentication using JWT tokens, and dynamic CSV report generation.

## Features

- **Data Analysis:**
  - Calculate total revenue, top-selling products, and quantities sold by category.
  - Utilizes Django ORM for efficient data retrieval and aggregation.

- **Reporting:**
  - Generate summary reports in CSV format with categories, total revenue, top products, and quantities sold.
  - Download reports directly from the application.

- **User Authentication:**
  - Secure login and sign-up system using JWT tokens.
  - Endpoints for user registration (`/signup/`) and login (`/login/`).

## Setup Instructions

### Requirements

- Python 3.12
- Django 5.0.6
- PostgreSQL (or another supported database)
- Git (optional, for cloning the repository)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ppinklesh/Stantech.git
   cd ecommerce_data_analysis
   ```

2. **Setup Python Virtual Environment**

   Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**

   Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**

   Configure database settings in `ecommerce/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations**

   Apply initial database migrations:

   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**

   Launch the Django development server:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000/`.

### Admin Interface

- Django provides a built-in admin interface for managing database records:
  
  ```bash
  python manage.py createsuperuser
  ```

- Access the admin interface at `http://localhost:8000/admin/` to manage users, products, and other data.

### Usage

- Navigate to `/summary_report_csv/` to download the CSV summary report.
- Navigate to `/summary_report/` to display summary report.
- Use `/signup/` and `/login/` endpoints for user registration and authentication.
