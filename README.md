# Event Management Platform Backend

A robust Django REST Framework-based backend system for managing large-scale events and workshops. This platform was successfully deployed on **octenium.com** via cPanel and handled **1000+ applications**, serving both React Native mobile and React web applications.

## 📋 Project Overview

The Event Management Platform Backend is a comprehensive solution designed to streamline event management operations, including:
- Workshop scheduling and management
- Participant registration and attendance tracking
- Certificate generation and distribution
- Speaker and partner management
- Real-time notifications and confirmations
- Attendance tracking and reporting

## 🚀 Key Features

### Event Management
- **Workshop Management**: Create, update, and manage multiple workshops with details like title, description, date, duration, and sessions
- **Speaker Management**: Manage speaker profiles with bio, images, and partner associations
- **Partner Integration**: Track and manage event partners
- **Registration System**: Handle workshop registrations with automatic email confirmations

### Security Features
- **Advanced Rate Limiting**: Implemented throttling mechanisms to prevent abuse:
  - Registration throttling (minute, hour, and day-based limits)
  - Login and authentication throttling
  - Email confirmation throttling
- **JWT Authentication**: Secure token-based authentication using djangorestframework-simplejwt
- **CORS Support**: Configured CORS headers for cross-origin requests
- **CSRF Protection**: Cross-site request forgery protection enabled
- **reCAPTCHA Integration**: Google reCAPTCHA for form protection
- **OTP Authentication**: Two-factor authentication via django-otp

### Attendance & Certification
- **Attendance Tracking**: Track participant attendance during events
- **Certificate Generation**: Auto-generate certificates for successful participants
- **Cloudinary Integration**: Cloud-based file storage for images and certificates

### API Documentation
- **Swagger/OpenAPI**: Auto-generated API documentation using drf-spectacular
- **RESTful Design**: Standard REST API endpoints for all operations

## 🛡️ Security Measures (Post-Attack Implementation)

Due to security challenges encountered during the event, the following security measures were implemented:
- **Rate Limiting**: Multi-level throttling on registration, login, and email confirmation endpoints
- **Input Validation**: Comprehensive validation for all user inputs
- **Email Verification**: Confirmation-based email validation for registrations
- **Token Management**: JWT-based authentication with refresh token rotation
- **Cloudinary Security**: Secure file upload and storage with validation

## 📱 Client Support

This backend API serves:
- **React Native Mobile Application**: Native mobile app for attandens scanning
- **React Web Application**: Full-featured web interface for desktop users

## 🏗️ Project Architecture

### Core Components
```
core/                  # Django project settings and configuration
├── settings.py       # Main configuration file
├── urls.py          # URL routing
├── wsgi.py          # WSGI application entry point
└── asgi.py          # ASGI application entry point

app_models/           # Data models and business logic
├── models.py        # Workshop, Registration, Certificate, etc.
├── signals.py       # Django signals for event handling
└── migrations/      # Database migrations

apis/                 # REST API endpoints
├── views.py         # API view handlers
├── serializers.py   # Data serialization
├── urls.py          # API routing
├── throttles.py     # Rate limiting configurations
└── utils.py         # Utility functions

otp_admin/           # OTP-based admin authentication
├── models.py        # OTP models
├── signals.py       # OTP signal handlers
└── views.py         # OTP views
```

### Data Models
- **Workshop**: Event/workshop information with scheduling details
- **Registration**: User registration for workshops with attendance type (online/on-site)
- **Speaker**: Speaker profiles associated with workshops
- **Partner**: Event partners and sponsors
- **Certificate**: Issued certificates for participants
- **Attendance**: Attendance records for tracking
- **Notification**: Email notifications and confirmations

## 🛠️ Technology Stack

### Backend Framework
- **Django 5.2.6**: Web framework
- **Django REST Framework 3.16.1**: API framework
- **Gunicorn 23.0.0**: Production WSGI server

### Authentication & Security
- **djangorestframework-simplejwt 5.5.1**: JWT authentication
- **django-otp 1.6.1**: One-time password authentication
- **django-recaptcha 4.1.0**: reCAPTCHA integration
- **django-cors-headers 4.8.0**: CORS handling
- **cryptography 45.0.7**: Cryptographic functions

### Database & Storage
- **SQLite3**: Development database
- **psycopg2-binary 2.9.10**: PostgreSQL adapter (production)
- **PyMySQL 1.1.2**: MySQL support
- **Cloudinary 1.44.1 & django-cloudinary-storage 0.3.0**: Cloud file storage

### API Documentation & Filtering
- **drf-spectacular 0.28.0**: OpenAPI/Swagger documentation
- **django-filter 25.1**: Advanced filtering capabilities

### Data Processing
- **pandas 2.3.2**: Data analysis and manipulation
- **openpyxl 3.1.5**: Excel file handling
- **numpy 2.3.3**: Numerical computing
- **qrcode 8.8**: QR code generation (for certificates)

### Utilities
- **Pillow 11.3.0**: Image processing
- **PyJWT 2.10.1**: JSON Web Token handling
- **requests 2.32.5**: HTTP library
- **python-decouple 3.8**: Environment configuration
- **whitenoise 6.10.0**: Static file serving
- **pytz 2025.2**: Timezone support

## 📊 Deployment Information

### Hosting
- **Platform**: Octenium.com via cPanel
- **Server**: Production-ready deployment with Gunicorn + Nginx/Apache

### Statistics
- **Handled Applications**: 1000+
- **Security Events**: Mitigated mid-event attack with enhanced security measures
- **Active Users**: Supports both mobile and web clients simultaneously

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Event_management_platform_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=your-database-url
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   RECAPTCHA_PUBLIC_KEY=your-public-key
   RECAPTCHA_PRIVATE_KEY=your-private-key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 📡 API Endpoints

### Workshops
- `GET /api/workshops/` - List active workshops for current week
- `GET /api/workshops/all/` - List all workshops
- `GET /api/workshops/<id>/` - Get workshop details

### Registrations
- `POST /api/registrations/` - Register for a workshop (rate-limited)
- `POST /api/registrations/confirm-email/` - Confirm registration email

### Speakers
- `GET /api/speakers/` - List all speakers
- `GET /api/speakers/<id>/` - Get speaker details

### Partners
- `GET /api/partners/` - List all partners
- `GET /api/partners/<id>/` - Get partner details

### Certificates
- `GET /api/certificates/<id>/` - Get certificate details

### Authentication
- `POST /api/token/` - Obtain JWT token (rate-limited)
- `POST /api/token/refresh/` - Refresh JWT token

### System
- `GET /api/health/` - Health check endpoint

## 🔒 Security Best Practices

### Implemented Measures
1. **Rate Limiting**: Prevents brute force attacks
   - Registration: Limited to prevent spam applications
   - Login: Protected with LoginThrottle
   - Email Confirmation: Limited to prevent abuse

2. **Input Validation**: All inputs validated before processing
   - Email format validation
   - Phone number length validation
   - Data type validation via serializers

3. **Token Security**: JWT with secure expiration
4. **HTTPS Enforcement**: Production deployments use HTTPS only
5. **CORS Restrictions**: Only whitelisted origins allowed
6. **Database Security**: Sensitive data encrypted where necessary

## 📝 Database Schema

### Key Relations
- Workshop → Speaker (Many-to-Many)
- Workshop → Partner (Foreign Key)
- Workshop → Registration (One-to-Many)
- Registration → Certificate (One-to-One)
- Registration → Attendance (One-to-Many)

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📚 API Documentation

Full API documentation available at:
```
http://localhost:8000/api/docs/
```

## 🤝 Contributing

Guidelines for contributors:
1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## 📄 License



## 📧 Support

For issues, questions, or suggestions, please contact the development team or visit the project repository.

---

**Last Updated**: December 10, 2025  
**Version**: 1.0.0  
**Status**: Production-Ready