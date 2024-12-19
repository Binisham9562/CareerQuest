from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm,JobPostEditForm
from django.contrib import messages
from datetime import datetime, timedelta
from userapp.models import JobApplication,EmployerProfile
from django.db.models import Count
from .models import JobPost
from dateutil.relativedelta import relativedelta
from django.utils import timezone

@login_required
def employer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users

    # Fetch jobs posted by the logged-in employer
    employer_jobs = JobPost.objects.filter(employer=request.user)

    # Make sure closing_date is timezone-aware for each job
    for job in employer_jobs:
        if job.closing_date and job.closing_date.tzinfo is None:  # Check if it's naive
            job.closing_date = timezone.make_aware(job.closing_date)  # Convert to aware datetime if it's naive

    # Fetch applications per job (for bar chart)
    applications_per_job = JobApplication.objects.filter(job__in=employer_jobs) \
        .values('job__job_title') \
        .annotate(application_count=Count('id'))

    # Convert applications_per_job to a JSON-serializable format
    applications_per_job_data = list(applications_per_job)

    # Fetch application trends over the last 6 months (for line chart)
    today = timezone.now()
    start_of_month = today.replace(day=1)

    applications_over_time = []
    for i in range(6):  # Last 6 months
        # Calculate start and end of the month, ensuring we handle timezone correctly
        start_date = (start_of_month - timedelta(days=30 * i)).replace(day=1)
        # Use the last day of the month as end_date
        end_date = (start_of_month - timedelta(days=30 * (i - 1))).replace(day=1) - timedelta(days=1) if i > 0 else today
        
        # Count applications in that month (filtering by applied_on)
        applications_count = JobApplication.objects.filter(
            applied_on__gte=start_date, applied_on__lt=end_date
        ).count()

        applications_over_time.append({
            'month': start_date.strftime('%b %Y'),
            'count': applications_count
        })

    # Additional data for dashboard
    total_job_posts = employer_jobs.count()
    total_applications = JobApplication.objects.filter(job__in=employer_jobs).count()
    jobs_expiring_soon = JobPost.objects.filter(closing_date__lt=datetime.today()).count()
    pending_actions = JobApplication.objects.filter(status='Pending').count()

    context = {
        'applications_per_job': applications_per_job_data,  # Pass the serializable data
        'applications_over_time': applications_over_time,
        'total_job_posts': total_job_posts,
        'total_applications': total_applications,
        'jobs_expiring_soon': jobs_expiring_soon,
        'pending_actions': pending_actions,
    }

    return render(request, 'employerapp/employer_dashboard.html', context)

@login_required
def post_job(request):
    try:
        employer_profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        messages.error(request, "You need to create an employer profile first.")
        return redirect('create_employer_profile')  # Redirect to profile creation page

    # Check if the employer's company is approved
    if employer_profile.status != 'approved':
        if employer_profile.status == 'pending':
            messages.error(request, "Your company profile is still pending admin approval. You cannot post jobs yet.")
        elif employer_profile.status == 'rejected':
            messages.error(request, "Your company profile has been rejected. Please contact admin for more details.")
        return redirect('employer_dashboard')  # Redirect to employer dashboard

    # Allow job posting if the company is approved
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user   # Associate the job with the employer profile
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = JobPostForm()

    return render(request, 'employerapp/post_job.html', {'form': form})

def employer_applications_view(request):
    # Fetch jobs posted by the logged-in employer
    employer_jobs = JobPost.objects.filter(employer=request.user)

    # Fetch applications for these jobs, ordered by most recent
    applications = JobApplication.objects.filter(job__in=employer_jobs).order_by('-applied_on')

    context = {
        'applications': applications,
    }
    return render(request, 'employerapp/employer_applications.html', context)

@login_required

def change_application_status(request, application_id):
    # Fetch the specific application
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        # Update the status based on the action
        if action == 'accept':
            application.status = 'accepted'
            messages.success(request, 'Application accepted successfully.')
        elif action == 'reject':
            application.status = 'rejected'
            messages.success(request, 'Application rejected successfully.')
        elif action == 'pending':
            application.status = 'pending'
            messages.info(request, 'Application set to pending.')

        # Save the updated status
        application.save()

        return redirect('employer_applications')  # Redirect to the applications list page

    # If GET request, render the status change page
    return render(request, 'employerapp/change_application_status.html', {'application': application})


def employer_jobs_view(request):
    """
    Display all jobs posted by the logged-in employer, ordered by post date.
    """
    user = request.user  # Logged-in User instance
    jobs = JobPost.objects.filter(employer=user).order_by('-post_date')  # Fetch employer's jobs
    return render(request, 'employerapp/employer_jobs.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    """
    Allows the logged-in employer to edit a job post.
    """
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)

    if request.method == 'POST':
        form = JobPostEditForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_jobs')  # Redirect back to the list of posted jobs
    else:
        form = JobPostEditForm(instance=job)

    return render(request, 'employerapp/edit_job_post.html', {'form': form, 'job': job})

@login_required

def close_job(request, job_id):
    # Get the job post by its ID
    job = get_object_or_404(JobPost, id=job_id)
    
    # Check if the logged-in user is the employer who posted the job
    if request.user == job.employer:  # Assuming 'employer' is the related field for the employer
        # Close the job (set is_active to False)
        job.is_active = False
        job.save()
        
        # Show a success message
        messages.success(request, f"Job '{job.job_title}' has been successfully closed.")
    else:
        # Show an error message if the user is not the employer of this job
        messages.error(request, "You are not authorized to close this job.")

    # Redirect back to the employer job listings page
    return redirect('employer_jobs')  # Make sure this UR


def enable_job(request, job_id):
    # Get the job post by its ID
    job = get_object_or_404(JobPost, id=job_id)
    
    # Check if the logged-in user is the employer who posted the job
    if request.user == job.employer:  # Assuming 'employer' is the related field for the employer
        # Set is_active to True to reopen the job
        job.is_active = True
        job.save()
        
        # Show a success message
        messages.success(request, f"Job '{job.job_title}' has been reopened.")
    else:
        # Show an error message if the user is not the employer of this job
        messages.error(request, "You are not authorized to reopen this job.")
    
    # Redirect back to the employer job listings page
    return redirect('employer_jobs')