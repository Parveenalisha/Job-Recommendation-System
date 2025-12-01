"""
Setup script for Job Recommendation System
Run this script to initialize the project
"""
import os
import sys
import subprocess

def run_command(command):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("Job Recommendation System - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print("\n1. Installing dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install dependencies")
        sys.exit(1)
    
    print("\n2. Creating migrations...")
    if not run_command("python manage.py makemigrations"):
        print("Failed to create migrations")
        sys.exit(1)
    
    print("\n3. Applying migrations...")
    if not run_command("python manage.py migrate"):
        print("Failed to apply migrations")
        sys.exit(1)
    
    print("\n4. Creating necessary directories...")
    os.makedirs("media/resumes", exist_ok=True)
    os.makedirs("media/profile_pics", exist_ok=True)
    os.makedirs("jobs/ml_models", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    print("Directories created successfully")
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Access the site: http://127.0.0.1:8000/")
    print("\nNote: The ML model will be created automatically on first job posting.")

if __name__ == "__main__":
    main()







