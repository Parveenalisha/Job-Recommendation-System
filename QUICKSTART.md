# Quick Start Guide

## Installation Steps

1. **Install Python 3.8+** (if not already installed)

2. **Navigate to project directory**:
```bash
cd job_recomm
```

3. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (optional)**:
```bash
python manage.py createsuperuser
```

7. **Run the server**:
```bash
python manage.py runserver
```

8. **Access the application**:
   - Open browser: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## First Steps

### As a Job Seeker:

1. Click **Register** → Create account (leave "Register as HR" unchecked)
2. Complete your profile with:
   - Full name, email, phone
   - Skills (comma-separated, e.g., "Python, Django, JavaScript")
   - Experience years
   - Education, location
   - Upload resume (optional)
3. Browse jobs or check **Recommendations** for personalized suggestions
4. Apply for jobs with a cover letter

### As an HR/Recruiter:

1. Click **Register** → Create account → **Check "Register as HR/Recruiter"**
2. Complete HR profile with company information
3. Click **Post Job** to create job listings
4. The ML system will automatically verify your job posting
5. View and manage applications in **Applications** section

## Features Overview

- ✅ User authentication (separate for job seekers and HR)
- ✅ Profile management
- ✅ Job posting and browsing
- ✅ ML-powered fake job detection
- ✅ Personalized job recommendations
- ✅ Job application system
- ✅ Application status tracking
- ✅ Beautiful Bootstrap UI

## Troubleshooting

**Issue**: Migration errors
- Solution: Delete `db.sqlite3` and run migrations again

**Issue**: ML model not working
- Solution: The model is created automatically on first job post. Check `jobs/ml_models/` directory exists.

**Issue**: Static files not loading
- Solution: Run `python manage.py collectstatic` (for production)

**Issue**: Media files not uploading
- Solution: Ensure `media/` directory exists with proper permissions

## Need Help?

Check the main README.md for detailed documentation.








