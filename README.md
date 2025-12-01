# Job Recommendation System

A comprehensive Django-based job recommendation system with ML-powered fake job detection, user profiles, job applications, and personalized job recommendations.

## Features

### For Job Seekers
- **User Registration & Profile**: Create detailed profiles with skills, experience, education, and resume upload
- **Job Browsing**: Search and filter jobs by location, type, experience level, and keywords
- **Personalized Recommendations**: Get job recommendations based on your skills, experience, and location
- **Job Applications**: Apply for jobs with cover letters
- **Application Tracking**: Track the status of your applications

### For HR/Recruiters
- **Separate HR Login**: Dedicated login system for HR/Recruiters
- **Company Profile**: Create and manage company profiles
- **Job Posting**: Post job openings with detailed descriptions and requirements
- **ML-Powered Verification**: Automatic fake job detection using machine learning
- **Application Management**: Review and manage applications, update application status
- **Job Management**: Edit and delete posted jobs

### ML Features
- **Fake Job Detection**: Machine learning model automatically verifies job postings
- **Confidence Scoring**: Each job gets a confidence score indicating authenticity
- **Real-time Prediction**: ML model runs when jobs are posted or updated

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5.3.0
- **ML**: scikit-learn, pandas, numpy
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Forms**: django-crispy-forms with Bootstrap 5

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser** (optional, for admin access):
```bash
python manage.py createsuperuser
```

7. **Run the development server**:
```bash
python manage.py runserver
```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
job_recomm/
├── job_recomm/          # Main project settings
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL configuration
│   └── ...
├── users/               # User management app
│   ├── models.py        # User, UserProfile, HRProfile models
│   ├── views.py         # Authentication and profile views
│   └── ...
├── jobs/                # Job management app
│   ├── models.py        # Job model
│   ├── views.py         # Job listing, posting, recommendations
│   ├── ml_model.py      # ML fake job detection
│   └── ...
├── applications/        # Job applications app
│   ├── models.py        # Application model
│   ├── views.py         # Application views
│   └── ...
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── jobs/            # Job-related templates
│   ├── users/           # User-related templates
│   └── applications/    # Application templates
└── static/              # Static files (CSS, JS, images)
```

## Usage Guide

### For Job Seekers

1. **Register**: Create an account (select "Job Seeker" option)
2. **Complete Profile**: Add your skills, experience, education, and upload resume
3. **Browse Jobs**: Use the search and filter options to find jobs
4. **Get Recommendations**: Visit the "Recommendations" page for personalized job suggestions
5. **Apply**: Click "Apply Now" on any job posting
6. **Track Applications**: View your applications and their status in "My Applications"

### For HR/Recruiters

1. **Register**: Create an account and select "Register as HR/Recruiter"
2. **Complete HR Profile**: Add company information
3. **Post Jobs**: Click "Post Job" and fill in job details
4. **Review ML Verification**: Check if your job is verified by the ML system
5. **Manage Applications**: Review applications in "Applications" section
6. **Update Status**: Change application status (Pending, Under Review, Shortlisted, etc.)

## ML Model Details

The fake job detection model uses:
- **TF-IDF Vectorization**: Converts job text into numerical features
- **Random Forest Classifier**: Classifies jobs as real or fake
- **Rule-based Features**: Additional features like salary info, experience requirements, suspicious words
- **Confidence Scoring**: Provides confidence percentage for predictions

The model is automatically trained on first run and saved for future use.

## Customization

### Changing Database

Edit `job_recomm/settings.py` to use PostgreSQL or MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Improving ML Model

To improve the fake job detection model:
1. Collect real training data
2. Update `jobs/ml_model.py` with better features
3. Retrain the model with more data

## Security Notes

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Implement proper file upload validation
- Add rate limiting for job postings

## Future Enhancements

- Email notifications for applications
- Advanced search with multiple filters
- Job alerts based on saved searches
- Resume parsing and auto-fill
- Integration with job boards
- Enhanced ML model with more training data
- User ratings and reviews
- Company pages with job listings

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the repository.







