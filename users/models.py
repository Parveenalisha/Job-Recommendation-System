from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model"""
    is_hr = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Profile for job seekers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(help_text="Comma-separated list of skills")
    experience_years = models.IntegerField(default=0)
    education = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name}'s Profile"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


class HRProfile(models.Model):
    """Profile for HR/Recruiters"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_profile')
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"







