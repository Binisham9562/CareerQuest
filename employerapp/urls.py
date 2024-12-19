from django.urls import path
from . import views


urlpatterns = [
     path('employer_dashboard/', views.employer_dashboard, name='employer_dashboard'),
     path('post_job/', views.post_job, name='post_job'),
     path('applications/', views.employer_applications_view, name='employer_applications'),
     path('applications/<int:application_id>/status/', views.change_application_status, name='change_application_status'),
     path('my-jobs/', views.employer_jobs_view, name='employer_jobs'),
     path('employer/edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
     path('close-job/<int:job_id>/', views.close_job, name='close_job'),
     path('enable_job/<int:job_id>/', views.enable_job, name='enable_job'),
]