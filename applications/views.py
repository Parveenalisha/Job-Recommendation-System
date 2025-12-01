from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    """Apply for a job"""
    if request.user.is_hr:
        messages.error(request, 'HR/Recruiters cannot apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if already applied
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    """View user's applications"""
    if request.user.is_hr:
        return redirect('hr_applications')
    
    applications = Application.objects.filter(user=request.user).order_by('-applied_date')
    return render(request, 'applications/my_applications.html', {'applications': applications})


@login_required
def application_detail(request, pk):
    """View application details"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions
    if application.user != request.user and not request.user.is_hr:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('home')
    
    # If HR, allow status update
    can_update_status = request.user.is_hr and application.job.posted_by == request.user
    
    if request.method == 'POST' and can_update_status:
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated!')
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationStatusForm(instance=application) if can_update_status else None
    
    return render(request, 'applications/application_detail.html', {
        'application': application,
        'form': form,
        'can_update_status': can_update_status,
    })


@login_required
def hr_applications(request):
    """View applications for HR's posted jobs"""
    if not request.user.is_hr:
        messages.error(request, 'Only HR/Recruiters can view this page.')
        return redirect('home')
    
    # Get all jobs posted by this HR
    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs).order_by('-applied_date')
    
    return render(request, 'applications/hr_applications.html', {'applications': applications})








