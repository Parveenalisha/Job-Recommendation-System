from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job
from .forms import JobPostForm, JobSearchForm
from .ml_model import detector
from users.models import UserProfile


def home(request):
    """Home page with job listings"""
    jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:10]
    form = JobSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        location = form.cleaned_data.get('location')
        job_type = form.cleaned_data.get('job_type')
        experience_level = form.cleaned_data.get('experience_level')
        
        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company_name__icontains=search) |
                Q(skills_required__icontains=search)
            )
        
        if location:
            jobs = jobs.filter(location__icontains=location)
        
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
    
    context = {
        'jobs': jobs,
        'form': form,
    }
    return render(request, 'jobs/home.html', context)


def job_list(request):
    """List all active jobs"""
    jobs = Job.objects.filter(is_active=True).order_by('-posted_date')
    form = JobSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        location = form.cleaned_data.get('location')
        job_type = form.cleaned_data.get('job_type')
        experience_level = form.cleaned_data.get('experience_level')
        
        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company_name__icontains=search) |
                Q(skills_required__icontains=search)
            )
        
        if location:
            jobs = jobs.filter(location__icontains=location)
        
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
    
    context = {
        'jobs': jobs,
        'form': form,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    """Job detail view"""
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    
    if request.user.is_authenticated and not request.user.is_hr:
        has_applied = job.applications.filter(user=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_post(request):
    """Post a new job (HR only)"""
    if not request.user.is_hr:
        messages.error(request, 'Only HR/Recruiters can post jobs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            
            # ML Prediction
            prediction = detector.predict(
                job.title,
                job.description,
                job.requirements,
                job.company_name
            )
            
            job.is_verified = prediction['is_real']
            job.ml_confidence = prediction['confidence']
            
            job.save()
            
            if prediction['is_real']:
                messages.success(request, f'Job posted successfully! (Verified: {prediction["confidence"]*100:.1f}% confidence)')
            else:
                messages.warning(request, f'Job posted but flagged as potentially fake. Please review. (Confidence: {prediction["confidence"]*100:.1f}%)')
            
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm()
    
    return render(request, 'jobs/job_post.html', {'form': form})


@login_required
def job_recommendations(request):
    """Get personalized job recommendations for user"""
    if request.user.is_hr:
        messages.info(request, 'Job recommendations are for job seekers only.')
        return redirect('home')
    
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile to get job recommendations.')
        return redirect('user_profile_create')
    
    user_skills = set(profile.get_skills_list())
    user_experience = profile.experience_years
    
    # Get all active jobs
    all_jobs = Job.objects.filter(is_active=True, is_verified=True)
    
    # Score jobs based on match
    job_scores = []
    for job in all_jobs:
        score = 0
        job_skills = set(job.get_skills_list())
        
        # Skill matching
        if user_skills and job_skills:
            common_skills = user_skills.intersection(job_skills)
            score += len(common_skills) * 10
        
        # Experience matching
        if job.experience_level == 'Entry' and user_experience <= 2:
            score += 5
        elif job.experience_level == 'Mid' and 2 < user_experience <= 5:
            score += 5
        elif job.experience_level == 'Senior' and user_experience > 5:
            score += 5
        
        # Location matching (if user has location)
        if profile.location and job.location:
            if profile.location.lower() in job.location.lower() or job.location.lower() in profile.location.lower():
                score += 3
        
        job_scores.append((job, score))
    
    # Sort by score and get top recommendations
    job_scores.sort(key=lambda x: x[1], reverse=True)
    # Get top 10 jobs with scores, normalize score to percentage (max score ~50)
    max_score = max([score for _, score in job_scores], default=1)
    recommended_jobs = [(job, min(int((score / max_score) * 100), 100)) for job, score in job_scores if score > 0][:10]
    
    context = {
        'recommended_jobs': recommended_jobs,
        'profile': profile,
    }
    return render(request, 'jobs/job_recommendations.html', context)


@login_required
def my_jobs(request):
    """View jobs posted by HR"""
    if not request.user.is_hr:
        messages.error(request, 'Only HR/Recruiters can view this page.')
        return redirect('home')
    
    jobs = Job.objects.filter(posted_by=request.user).order_by('-posted_date')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def job_edit(request, pk):
    """Edit a job posting"""
    job = get_object_or_404(Job, pk=pk)
    
    if job.posted_by != request.user or not request.user.is_hr:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            
            # Re-run ML prediction
            prediction = detector.predict(
                job.title,
                job.description,
                job.requirements,
                job.company_name
            )
            
            job.is_verified = prediction['is_real']
            job.ml_confidence = prediction['confidence']
            job.save()
            
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)
    
    return render(request, 'jobs/job_post.html', {'form': form, 'edit': True, 'job': job})


@login_required
def job_delete(request, pk):
    """Delete a job posting"""
    job = get_object_or_404(Job, pk=pk)
    
    if job.posted_by != request.user or not request.user.is_hr:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('home')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('my_jobs')
    
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

