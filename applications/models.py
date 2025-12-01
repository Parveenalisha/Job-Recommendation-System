from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()


class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, help_text="HR notes (not visible to applicant)")
    
    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.job.title}"








