# Mobile Stroke Unit and Remote Neurologist Consultation System

A Django-based web application for mobile stroke units and remote neurologist consultations.

## Features

- Patient data collection and management
- Remote neurologist consultation system
- Real-time alerts and notifications
- HIPAA-compliant data storage
- Comprehensive patient records
- NHISS scoring system
- Medical imaging management
- Vital signs tracking

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `stroke_system/` - Main project configuration
- `patients/` - Patient management app
- `neurologists/` - Neurologist consultation app
- `alerts/` - Alert and notification system
- `api/` - REST API endpoints

## Security

This application follows HIPAA compliance guidelines and implements:
- Data encryption
- Access control
- Audit logging
- Secure authentication

## License

This project is licensed under the MIT License. 