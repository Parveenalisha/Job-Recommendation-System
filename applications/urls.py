from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('hr/applications/', views.hr_applications, name='hr_applications'),
]







