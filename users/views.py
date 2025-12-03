from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, HRProfileForm
from .models import UserProfile, HRProfile
from django.contrib.auth import logout


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            
            # Redirect based on user type
            if user.is_hr:
                return redirect('hr_profile_create')
            else:
                return redirect('user_profile_create')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_profile_create(request):
    """Create user profile"""
    if request.user.is_hr:
        return redirect('hr_profile_create')
    
    if hasattr(request.user, 'profile'):
        return redirect('user_profile')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    return render(request, 'users/user_profile_form.html', {'form': form})


@login_required
def user_profile(request):
    """View user profile"""
    if request.user.is_hr:
        return redirect('hr_profile')
    
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect('user_profile_create')
    
    return render(request, 'users/user_profile.html', {'profile': profile})


@login_required
def user_profile_edit(request):
    """Edit user profile"""
    if request.user.is_hr:
        return redirect('hr_profile_edit')
    
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect('user_profile_create')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/user_profile_form.html', {'form': form, 'edit': True})


@login_required
def hr_profile_create(request):
    """Create HR profile"""
    if not request.user.is_hr:
        return redirect('user_profile_create')
    
    if hasattr(request.user, 'hr_profile'):
        return redirect('hr_profile')
    
    if request.method == 'POST':
        form = HRProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'HR Profile created successfully!')
            return redirect('hr_profile')
    else:
        form = HRProfileForm()
    return render(request, 'users/hr_profile_form.html', {'form': form})


@login_required
def hr_profile(request):
    """View HR profile"""
    if not request.user.is_hr:
        return redirect('user_profile')
    
    try:
        profile = request.user.hr_profile
    except HRProfile.DoesNotExist:
        return redirect('hr_profile_create')
    
    return render(request, 'users/hr_profile.html', {'profile': profile})


@login_required
def hr_profile_edit(request):
    """Edit HR profile"""
    if not request.user.is_hr:
        return redirect('user_profile_edit')
    
    try:
        profile = request.user.hr_profile
    except HRProfile.DoesNotExist:
        return redirect('hr_profile_create')
    
    if request.method == 'POST':
        form = HRProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'HR Profile updated successfully!')
            return redirect('hr_profile')
    else:
        form = HRProfileForm(instance=profile)
    return render(request, 'users/hr_profile_form.html', {'form': form, 'edit': True})

from django.contrib.auth import logout

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')







