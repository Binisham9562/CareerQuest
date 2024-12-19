# forms.py
from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_title', 'company_name', 'job_description', 'qualifications', 'requirements', 'location', 'salary_range', 'job_type', 'closing_date']
        widgets = {
            'closing_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
class JobPostEditForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_title', 'job_description', 'qualifications', 'requirements', 'location',
                  'salary_range', 'job_type', 'closing_date', 'is_active']
        widgets = {
            'closing_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom form control classes to all fields except 'closing_date'
        for field in self.fields:
            if field != 'closing_date':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
