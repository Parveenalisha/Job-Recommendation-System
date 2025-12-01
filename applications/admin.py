from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('user__username', 'job__title', 'job__company_name')
    readonly_fields = ('applied_date',)







