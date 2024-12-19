from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm, JobSeekerProfileForm, EmployerProfileForm
from .forms import EditAboutMeForm, EditSkillsForm, EditExperienceForm,EditQualificationForm, EditJobPreferencesForm, EditResumeForm,UpdateProfilePictureForm
from .models import JobSeekerProfile,EmployerProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm 
from employerapp.models import JobPost
from .forms import JobApplicationForm
from .models import JobApplication
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.db.models import Q


def frontpage(request):
    return render(request,'userapp/frontpage.html')
def home(request):
    user_data = request.session.get('user_data', {})  # Retrieve user-specific data from session
    return render(request, 'userapp/home.html', {'user_data': user_data})

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Save the user
            user = register_form.save()

            # Authenticate the user
            user = authenticate(username=user.username, password=register_form.cleaned_data.get('password1'))
            login(request, user)

            # Redirect to the question page to identify the user type
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the form errors.")
    else:
        register_form = RegisterForm()
    return render(request, 'userapp/register.html', {'form': register_form})
@login_required

def create_profile(request):
    """
    Asks the user whether they are an employer or a job seeker.
    Redirects them to the respective profile creation page based on the answer.
    """
    if request.method == 'POST':
        is_employer = request.POST.get('is_employer')

        if is_employer == 'yes':
            return redirect('create_employer_profile')  # Redirect to Employer profile creation
        elif is_employer == 'no':
            return redirect('create_job_seeker_profile')  # Redirect to Job Seeker profile creation
        else:
            messages.error(request, "Please answer the question to proceed.")  # If not selected, show an error
            return redirect('create_profile')

    return render(request, 'userapp/identify_user_type.html')

def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()  # Authenticate the user
            login(request, user)   # Log the user in
            
            if hasattr(user, 'job_seeker_profile'):
                # Redirect to Job Seeker dashboard
                return redirect('jobseeker_dashboard')
            elif hasattr(user, 'employer_profile'):
                # Redirect to Employer dashboard
                return redirect('employer_dashboard')
            else:
                # Redirect to profile creation page if no profile exists
                return redirect('create_profile')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'userapp/login.html', {'form': form})
@login_required

def create_job_seeker_profile(request):
    if request.method == 'POST':
        profile_form = JobSeekerProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # Create a user profile for Job Seeker
            profile_form.save(user = request.user)
            messages.success(request, "Job Seeker profile created successfully!")
            return redirect('view_profile_jobseeker')
    else:
        profile_form = JobSeekerProfileForm()
    return render(request, 'userapp/job_seeker_profile.html', {'form': profile_form})
@login_required

def create_employer_profile(request):
    if request.method == 'POST':
        profile_form = EmployerProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_form.save(user=request.user)
            messages.success(request, "Employer profile created successfully!")
            return redirect('view_profile_employer')
    else:
        profile_form = EmployerProfileForm()
    return render(request, 'userapp/employer_profile.html', {'form': profile_form})

@login_required
def profile_view_employer(request):
    """
    Displays the user's profile based on their user type.
    """
    try:
        profile = EmployerProfile.objects.get(user=request.user)
        return render(request, 'userapp/employer_profile_view.html', {'profile': profile})
    except EmployerProfile.DoesNotExist:
        # If profile does not exist, redirect to profile creation question
        return redirect('home')
    
@login_required
def profile_view_jobseeker(request):
    """
    Displays the user's profile based on their user type.
    """
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
        return render(request, 'userapp/view_profile.html', {'profile': profile})
    except JobSeekerProfile.DoesNotExist:
        # If profile does not exist, redirect to profile creation question
        return redirect('home')
    

@login_required
def edit_about_me(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditAboutMeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditAboutMeForm(instance=profile)
    
    return render(request, 'userapp/edit_about_me.html', {'form': form})

@login_required
def edit_skills(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditSkillsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditSkillsForm(instance=profile)
    
    return render(request, 'userapp/edit_skills.html', {'form': form})

@login_required
def edit_experience(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditExperienceForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditExperienceForm(instance=profile)
    
    return render(request, 'userapp/edit_experience.html', {'form': form})

@login_required
def edit_qualification(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditQualificationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditQualificationForm(instance=profile)
    
    return render(request, 'userapp/edit_qualification.html', {'form': form})

@login_required
def edit_job_preferences(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditJobPreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditJobPreferencesForm(instance=profile)
    
    return render(request, 'userapp/edit_job_preferences.html', {'form': form})

@login_required
def edit_resume(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    
    if request.method == 'POST':
        form = EditResumeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile_jobseeker')
    else:
        form = EditResumeForm(instance=profile)
    
    return render(request, 'userapp/edit_resume.html', {'form': form})

@login_required
def update_profile_picture(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user) # Adjust based on your user-profile relation
    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('view_profile_jobseeker')  # Replace with your profile view URL
    else:
        form = UpdateProfilePictureForm(instance=profile)
    return render(request, 'userapp/update_profile_picture.html', {'form': form})

@login_required
def jobseeker_dashboard(request):
    user = request.user
    jobs = JobPost.objects.all() 
    context = {
        'user': user,
        'jobs': jobs
    } # Get all job posts
    return render(request, 'userapp/jobseeker_dashboard.html', context)

def job_detail(request, job_id):
    job = JobPost.objects.get(id=job_id)
    return render(request, 'userapp/job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Associate the logged-in user
            application.job = job  # Link the application to the job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('jobseeker_dashboard')  # Redirect after successful application
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()

    return render(request, 'userapp/apply_job.html', {'form': form, 'job': job})

def my_applications(request):
    # Fetch all job applications for the logged-in user
    applications = JobApplication.objects.filter(user=request.user).order_by('-applied_on')

    return render(request, 'userapp/my_applications.html', {
        'applications': applications
    })

@login_required
def account_settings(request):
    user = request.user
    
    # If the request is a POST request, handle password change or account deletion
    if request.method == 'POST':
        # Handling password change
        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Keep user logged in after password change
                messages.success(request, 'Password changed successfully.')
            else:
                messages.error(request, 'Error changing password. Please try again.')

        # Handling account deletion
        elif 'delete_account' in request.POST:
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')  # Redirect to home page or another page

    else:
        # If GET request, display the password change form
        password_form = CustomPasswordChangeForm(user=user)
    
    return render(request, 'userapp/account_settings.html', {
        'password_form': password_form,
        'user': user,
    })

@login_required
def logout_view(request):
    logout(request)  # Logs out the current user
    return redirect('home')  #


def search_results(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    results = []

    if query:
        # Filter JobPost model using Q objects to match multiple fields
        results = JobPost.objects.filter(
            Q(job_title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(qualifications__icontains=query) |
            Q(requirements__icontains=query) |
            Q(location__icontains=query)
        ).filter(is_active=True)  # Include only active job posts

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'userapp/search_results.html', context)

def about(request):
    return render(request, 'userapp/about.html')

def contact(request):
    return render(request, 'userapp/contact.html')

def privacy(request):
    return render(request, 'userapp/privacy.html')

def terms(request):
    return render(request, 'userapp/terms.html')