from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, HRProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_hr', 'is_job_seeker', 'is_staff')
    list_filter = ('is_hr', 'is_job_seeker', 'is_staff', 'is_superuser')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'location', 'experience_years')
    search_fields = ('full_name', 'email', 'skills')


@admin.register(HRProfile)
class HRProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'email', 'location')
    search_fields = ('company_name', 'email')








