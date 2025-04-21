Herly School Portal
A comprehensive school management system built with Django for primary and secondary schools. It includes full role-based access for administrators, teachers, students, and parents. The system supports timetables, attendance tracking, grading, communication, and visual analytics.

Features

- Role-Based Access (Admin, Teacher, Student, Parent)
- Class and Section Management
- Student & Teacher Management
- Timetable and School Calendar
- Attendance and Grade Reporting
- Fee and Exam Management
- Notifications via Email and SMS
- Export Reports to Excel/PDF
- Responsive UI with Mobile Support
- Graphical Analytics for Performance and Attendance

Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Database:  PostgreSQL
- Charts: Chart.js
- Notifications: SMTP Email, SMS API 

Installation

Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

Setup Instructions

# Clone the repository
git clone https://github.com/kheen-11/h_portals.git
cd h_portals

# Create and activate virtual environment
python -m venv env
source env/bin/activate   # For Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

Dashboards Overview

Admin Dashboard

Sidebar Navigation:
- Dashboard (Graphical Analytics)
- Class Management
- Student Management
- Teacher Management
- Parent Management
- Exam Management
- Attendance Tracking
- Grade Reports
- Fee Management
- Section Management
- Timetable Management
- School Calendar
- Settings

Main Panel:
- Graphical representation of attendance and performance trends
- Quick access to reports and system notifications

Teacher Dashboard

Sidebar Navigation:
- My Classes
- Attendance Management
- Assignment Uploads
- Exam Questions
- Grade Submission
- School Calendar

Main Panel:
- Class schedules and upcoming tasks
- Recent student submissions

Student Dashboard

Sidebar Navigation:
- My Timetable
- Exam Schedule
- Attendance Report
- Assignment Submissions
- School Calendar
- Report Card

Main Panel:
- Upcoming exams and assignments
- Notifications

Parent Dashboard

Sidebar Navigation:
- Child’s Attendance
- Fee Notifications
- Exam Results
- School Calendar

Main Panel:
- Performance insights and important notifications

Folder Structure

school_portal/
│
├── accounts/         # Authentication and user roles
├── core/             # Shared models and utilities
├── students/         # Student-specific features
├── teachers/         # Teacher-specific features
├── parents/          # Parent-specific features
├── static/           # Static files
├── templates/        # HTML templates
├── media/            # Uploaded files
├── manage.py
└── requirements.txt

Testing

python manage.py test

Deployment

To deploy in production:
- Set DEBUG=False
- Use ALLOWED_HOSTS
- Use environment variables for secrets
- Configure a production database
- Use Gunicorn and Nginx for hosting
- Set up email and SMS services

License


Contact

Developer: Mustapha Muhammad Lawal
Email: lawalmustapha455@gmail.com
GitHub: https://github.com/kheeng-11
