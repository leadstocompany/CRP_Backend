from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from django import forms
import secrets

from .models import License, LicenseAssignment


# ===============================
# Custom Admin Form for License
# ===============================
class LicenseAdminForm(forms.ModelForm):
    """
    Custom form to enforce validation rules in the Django admin interface
    for mutually exclusive is_trial and is_paid flags.
    """
    class Meta:
        model = License
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_trial = cleaned_data.get('is_trial')
        is_paid = cleaned_data.get('is_paid')

        # Ensure only one flag is selected
        if is_trial and is_paid:
            raise forms.ValidationError("A license cannot be both Trial and Paid.")
        if not is_trial and not is_paid:
            raise forms.ValidationError("You must select either Trial or Paid.")
        return cleaned_data


# ===============================
# Admin for License Model
# ===============================
@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    form = LicenseAdminForm

    # Fields shown in list view
    list_display = (
        'license_key', 'license_type', 'get_holder', 'is_trial', 'is_paid',
        'status', 'start_date', 'end_date', 'current_users_count', 'max_users_allowed'
    )

    # Read-only fields in form
    readonly_fields = (
        'license_key', 'created_at', 'generate_license_button', 'current_users_count'
    )

    # Fields shown in form layout
    fields = (
        'license_type', 'company', 'user',
        'is_trial', 'is_paid', 'status',
        'start_date', 'end_date',
        'current_users_count', 'max_users_allowed',
        'license_key', 'generate_license_button', 'created_at',
    )
    search_fields = ['license_key']

    # Custom bulk admin actions
    actions = ['generate_license_action']

    # Helper to show company or user name in list
    def get_holder(self, obj):
        if obj.license_type == 'company' and obj.company:
            return f"Company: {obj.company.company_name}"
        elif obj.license_type == 'individual' and obj.user:
            return f"User: {obj.user.username}"
        return "-"
    get_holder.short_description = 'Licensed To'

    # Bulk action to generate and activate licenses
    def generate_license_action(self, request, queryset):
        """
        Admin bulk action: generate license keys for selected records.
        """
        for license in queryset:
            if not license.license_key:
                license.license_key = secrets.token_urlsafe(12).upper()[:12]
            license.status = 'active'
            license.start_date = timezone.now().date()
            license.end_date = license.start_date + timezone.timedelta(days=365)
            license.is_trial = False
            license.is_paid = True
            license.save()
        self.message_user(request, "Selected licenses generated and activated.")
    generate_license_action.short_description = "Generate license key and activate"

    # Button displayed in admin to trigger manual license key generation
    def generate_license_button(self, obj):
        if obj.pk and not obj.license_key:
            return format_html(
                '<a class="button" href="{}">Generate License</a>',
                f'generate-license/{obj.pk}'
            )
        elif obj.pk and obj.license_key:
            return format_html('<span style="color: green;">✔ License already generated</span>')
        return "-"
    generate_license_button.short_description = "Manual License Generation"

    # Add custom admin URL for license generation
    def get_urls(self):
        """
        Extend default admin URLs to include a custom license generation route.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-license/<int:license_id>',
                self.admin_site.admin_view(self.generate_license_view),
                name='generate-license',
            ),
        ]
        return custom_urls + urls

    # View that handles generation logic for the custom admin button
    def generate_license_view(self, request, license_id):
        """
        Admin view handler to generate a license key and activate the license.
        Redirects back to the change form.
        """
        license = License.objects.get(pk=license_id)

        if license.license_key:
            self.message_user(request, "License already generated.", level=messages.WARNING)
        else:
            license.license_key = secrets.token_urlsafe(12).upper()[:12]
            license.status = 'active'
            license.start_date = timezone.now().date()
            license.end_date = license.start_date + timezone.timedelta(days=365)
            license.is_trial = False
            license.is_paid = True
            license.save()
            self.message_user(request, "License generated and activated.", level=messages.SUCCESS)

        return redirect(f'/admin/licenses/license/{license_id}/change/')


# ===============================
# Admin for LicenseAssignment
# ===============================
@admin.register(LicenseAssignment)
class LicenseAssignmentAdmin(admin.ModelAdmin):
    """
    Admin panel for tracking which users are assigned to which licenses.
    Useful for company license seat tracking.
    """
    list_display = ('license', 'user', 'assigned_at')
    search_fields = ('license__license_key', 'user__username')
    autocomplete_fields = ['user', 'license']
