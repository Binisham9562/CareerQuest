from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_description = models.TextField()
    qualifications = models.TextField()  # Add qualifications as a new field
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255, blank=True, null=True) 
    job_type_choices = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]
    job_type = models.CharField(max_length=20, choices=job_type_choices)
    post_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)  # To mark if the job post is still active
    employer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='job_posts')  # Link to the Employer (User model)

    def __str__(self):
        return self.job_title

    class Meta:
        verbose_name = 'Job Post'
        verbose_name_plural = 'Job Posts'
