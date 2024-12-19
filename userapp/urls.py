from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('home/',views.home,name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('create-job-seeker-profile/', views.create_job_seeker_profile, name='create_job_seeker_profile'),
    path('create-employer-profile/', views.create_employer_profile, name='create_employer_profile'),
    path('create_profile/', views.create_profile, name='create_profile'), 
    path('profile/', views.profile_view_jobseeker, name='view_profile_jobseeker'),
    path('employer_profile/', views.profile_view_employer, name='view_profile_employer'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/about/', views.edit_about_me, name='edit_about_me'),
    path('profile/edit/skills/', views.edit_skills, name='edit_skills'),
    path('profile/edit/experience/', views.edit_experience, name='edit_experience'),
    path('profile/edit/qualification/', views.edit_qualification, name='edit_qualification'),
    path('profile/edit/job-preferences/', views.edit_job_preferences, name='edit_job_preferences'),
    path('profile/edit/resume/', views.edit_resume, name='edit_resume'),
    path('profile/edit/update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),   
    path('jobseeker_dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_results, name='search_results'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
   
]