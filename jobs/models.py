from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
        ('Executive', 'Executive'),
    ]
    
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full-time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='Entry')
    skills_required = models.TextField(help_text="Comma-separated list of required skills")
    is_remote = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # ML prediction result
    ml_confidence = models.FloatField(default=0.0, help_text="ML model confidence score")
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"
    
    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'pk': self.pk})
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills_required:
            return [skill.strip() for skill in self.skills_required.split(',')]
        return []
    
    def get_salary_range(self):
        """Return formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f}"
        elif self.salary_min:
            return f"${self.salary_min:,.0f}+"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f}"
        return "Not specified"








