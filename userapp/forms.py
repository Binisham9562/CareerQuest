from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobSeekerProfile,EmployerProfile
import json
from .models import JobApplication
from django.contrib.auth.forms import PasswordChangeForm

# Registration Form (No explicit user_type field)
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

# Job Seeker Profile Form
class JobSeekerProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # Optional profile picture
    about_me = forms.CharField(widget=forms.Textarea, required=True)
    github_link = forms.URLField(max_length=200, required=False)  # Make GitHub link optional
    linkedin_link = forms.URLField(max_length=200, required=False)  # Make LinkedIn link optional
    resume = forms.FileField(required=True)
    skills = forms.CharField(widget=forms.Textarea, required=True)
    qualification = forms.CharField(max_length=200, required=True)
    experience = forms.CharField(widget=forms.Textarea, required=False)  # Optional
    job_preferences = forms.CharField(widget=forms.Textarea, required=True)
    preferred_location = forms.CharField(max_length=100, required=True)

    class Meta:
        model = JobSeekerProfile
        fields = ['profile_picture', 'about_me', 'github_link', 'linkedin_link', 'resume', 'skills', 'qualification', 'experience', 'job_preferences', 'preferred_location']
        widgets = {
            'github_link': forms.URLInput(attrs={'placeholder': 'Enter GitHub Link (Optional)'}),
            'linkedin_link': forms.URLInput(attrs={'placeholder': 'Enter LinkedIn Link (Optional)'}),
        }

    def save(self, commit=True, user=None):
        profile = super().save(commit=False)
        if user:
            profile.user = user  # Associate with the current user
        if commit:
            profile.save()  # Save the profile
        return profile
# Employer Profile Form
class EmployerProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length=100, required=True)
    company_description = forms.CharField(widget=forms.Textarea, required=True)
    company_logo = forms.ImageField(required=False)
    industry_type = forms.CharField(max_length=100, required=True)
    company_location = forms.CharField(max_length=200, required=True)
    company_size = forms.ChoiceField(choices=[('1-10', '1-10'), ('11-50', '11-50'), ('51-200', '51-200'), ('200+', '200+')], required=True)
    website_url = forms.URLField(max_length=200, required=True)
    social_media_links = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Enter social media links in the format: {'Facebook': 'https://facebook.com'}"}),
        required=False,
        help_text="Enter social media links in the format: {'platform': 'URL'}"
    )

    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_logo', 'industry_type', 
                  'company_location', 'company_size', 'website_url', 'social_media_links']

    def clean_social_media_links(self):
        social_media_links = self.cleaned_data.get('social_media_links')
        if social_media_links:
            try:
                # Try to parse the JSON input
                social_media_links = json.loads(social_media_links)
                if not isinstance(social_media_links, dict):
                    raise forms.ValidationError("Social media links must be in a key-value format (e.g., {'Facebook': 'URL'})")
                
                # Optionally, validate the URLs for proper format
                for key, value in social_media_links.items():
                    if not value.startswith('http'):
                        raise forms.ValidationError(f"The URL for {key} must start with 'http'.")
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format. Please provide the data in the correct format (e.g., {'Facebook': 'https://facebook.com'})")
        return social_media_links

    def save(self, user=None, commit=True):
        profile = super().save(commit=False)
        if user:
            profile.user = user
        
        # Convert social media links from string to JSON before saving
        if self.cleaned_data['social_media_links']:
            profile.social_media_links = self.cleaned_data['social_media_links']
        
        if commit:
            profile.save()
        return profile

# Simple Profile Form for Role Selection
class ProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['profile_picture', 'about_me', 'skills', 'github_link', 'linkedin_link']


class EditAboutMeForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['about_me']
        widgets = {
            'about_me': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write something about yourself...',
                    'rows': 4,
                }
            ),
        }

class EditSkillsForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['skills']
        widgets = {
            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'List your skills, separated by commas...',
                    'rows': 3,
                }
            ),
        }

class EditExperienceForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['experience']
        widgets = {
            'experience': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe your professional experience...',
                    'rows': 5,
                }
            ),
        }

class EditQualificationForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['qualification']
        widgets = {
            'qualification': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your qualifications...',
                }
            ),
        }

class EditJobPreferencesForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['job_preferences', 'preferred_location']  # Include both fields
        widgets = {
            'job_preferences': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your preferred job...',
                }
            ),
            'preferred_location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your preferred location...',
                }
            ),
        }


class EditResumeForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
        }

class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))