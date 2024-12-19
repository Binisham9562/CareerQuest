from django.contrib import admin
from .models import EmployerProfile

# Custom actions to approve or reject companies
def approve_companies(modeladmin, request, queryset):
    queryset.update(status='approved')

def reject_companies(modeladmin, request, queryset):
    queryset.update(status='rejected')

# Setting short descriptions for actions
approve_companies.short_description = "Approve selected companies"
reject_companies.short_description = "Reject selected companies"

class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'status', 'company_location', 'industry_type', 'user')
    list_filter = ('status', 'industry_type')
    search_fields = ('company_name', 'company_location', 'industry_type')
    
    # Allow editing of status field in the admin
    fields = ('company_name', 'company_description', 'company_logo', 'industry_type', 'company_location', 'company_size', 'website_url', 'social_media_links', 'status')
    readonly_fields = ('user',)  # Make the user field read-only if it's set automatically

    # Add the custom actions to the admin panel
    actions = [approve_companies, reject_companies]

admin.site.register(EmployerProfile, EmployerProfileAdmin)

