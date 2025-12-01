from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'posted_by', 'location', 
                    'is_verified', 'ml_confidence', 'is_active', 'posted_date')
    list_filter = ('is_verified', 'is_active', 'job_type', 'experience_level', 'posted_date')
    search_fields = ('title', 'company_name', 'description', 'location')
    readonly_fields = ('ml_confidence', 'posted_date', 'updated_date')







