# 🦷 Dental Practice Management System (DPMS)

A comprehensive web-based dental practice management system built with Django that helps dental professionals manage patients, appointments, payments, and medical records efficiently.

## ✨ Features

### 🏥 Patient Management
- **Patient Registration**: Add new patients with personal information
- **Patient Profiles**: Store patient photos, contact details, and medical notes
- **Patient Search**: Quick access to patient records and history
- **Patient History**: Track all patient interactions and treatments

### 💰 Payment Management
- **Payment Tracking**: Monitor total treatment costs and payments
- **Payment Records**: Keep detailed payment history for each patient
- **Outstanding Balances**: Automatically calculate remaining amounts
- **Payment Updates**: Real-time payment status tracking

### 📋 Visit Management
- **Visit Scheduling**: Schedule and track patient visits
- **Visit Notes**: Document treatment details and observations
- **Visit History**: Complete visit timeline for each patient
- **Treatment Records**: Link visits with payments and X-rays

### 🩺 Medical Records
- **X-Ray Management**: Upload and store patient X-ray images
- **Image Organization**: Automatic categorization of medical images
- **Secure Storage**: Protected access to sensitive medical data
- **Image Linking**: Connect X-rays with specific visits

### 🔐 Security & Authentication
- **User Authentication**: Secure login/logout system
- **Admin Panel**: Django admin interface for system management
- **Data Protection**: Secure handling of patient information
- **Access Control**: Role-based access to sensitive data

## 🛠️ Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow (PIL)
- **Environment Management**: django-environ
- **Authentication**: Django's built-in auth system

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <https://github.com/mo-hossam-stack/orthodontic_patient_portal>
cd orthodontic_patient_portal
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv env
env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root directory:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 5. Database Setup

```bash
# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
orthodontic_patient_portal/
├── dental_management/          # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── patients/                  # Patients app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Form definitions
│   ├── admin.py              # Admin interface
│   └── templates/            # HTML templates
│       └── patients/
├── media/                     # User uploaded files
│   └── patients/
│       ├── photos/           # Patient photos
│       └── xrays/            # X-ray images
├── templates/                 # Global templates
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🎯 Usage Guide

### Accessing the System

1. **Login**: Navigate to the login page and enter your credentials
2. **Dashboard**: View overview of patients and recent activities
3. **Patient Management**: Add, edit, and manage patient records
4. **Payments**: Track patient payments and outstanding balances
5. **Visits**: Schedule and record patient visits
6. **X-Rays**: Upload and manage patient X-ray images

### Key Features Walkthrough

#### Adding a New Patient
1. Click "Add New Patient" from the dashboard
2. Fill in patient details (name, phone, photo, notes)
3. Save the patient record

#### Recording a Payment
1. Navigate to the patient's detail page
2. Click "Add Payment"
3. Enter payment amount and details
4. System automatically calculates remaining balance

#### Scheduling a Visit
1. Select a patient
2. Click "Add Visit"
3. Set visit date and add notes
4. Optionally link X-ray images

#### Managing X-Rays
1. Upload X-ray images through the patient interface
2. Images are automatically organized by patient
3. Link X-rays to specific visits for better tracking

## 🔧 Configuration

### Production Deployment

For production deployment, update your `.env` file:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (PostgreSQL recommended for production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Static Files

```bash
python manage.py collectstatic
```

### Database Backup

```bash
python manage.py dumpdata > backup.json
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/mo-hossam-stack/orthodontic_patient_portal/issues) page
2. Create a new issue with detailed information
3. Contact the development team


## 🙏 Acknowledgments

- Django community for the excellent framework
- Contributors and testers
- Dental professionals for feedback and suggestions

---

**Note**: This system is designed for dental practice management. Ensure compliance with local healthcare data protection regulations (HIPAA, GDPR, etc.) when deploying in production.
