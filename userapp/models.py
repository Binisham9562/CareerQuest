from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from employerapp.models import JobPost



class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    
    # Fields for Job Seekers
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    job_preferences = models.TextField(blank=True, null=True)
    preferred_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} (Job Seeker)"


class EmployerProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employerprofile")
    
    # Fields for Employers
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True, null=True)
    company_location = models.CharField(max_length=200, blank=True, null=True)
    company_size = models.CharField(
        max_length=50, 
        choices=[
            ('1-10', '1-10'), 
            ('11-50', '11-50'), 
            ('51-200', '51-200'), 
            ('200+', '200+')
        ], 
        blank=True, null=True
    )
    website_url = models.URLField(max_length=200, blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True, default=dict)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')

    def __str__(self):
        return f"{self.user.username} (Employer), {self.company_name or 'No Company Name'}"

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}"        
