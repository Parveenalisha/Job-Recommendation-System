from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/create/', views.user_profile_create, name='user_profile_create'),
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('hr/profile/', views.hr_profile, name='hr_profile'),
    path('hr/profile/create/', views.hr_profile_create, name='hr_profile_create'),
    path('hr/profile/edit/', views.hr_profile_edit, name='hr_profile_edit'),
]







