# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import UserProfile

User = get_user_model()
admin.site.site_header = "CRP System Administration"
admin.site.site_title = "CRP Admin Portal"
admin.site.index_title = "Welcome to the CRP Admin Dashboard"
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fieldsets = (
        ("Profile Information", {
            "fields": ('company', 'user_type', 'designation'),
        }),
        ("Contact Details", {
            "fields": ('mobile_number1', 'mobile_number2', 'address1', 'address2', 'town_city', 'state', 'country', 'zipcode'),
        }),
        ("OTP Settings", {
            "fields": ('otp_via_email', 'entered_otp'),
        }),
    )

    def save_model(self, request, obj, form, change):
        profile = obj.userprofile
        if profile.otp_via_email:
            # Validate OTP
            if profile.otp_code != profile.entered_otp:
                raise ValidationError("Entered OTP does not match the generated OTP.")
        super().save_model(request, obj, form, change)

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Unregister the original UserAdmin
admin.site.unregister(User)

# Register the User model with the new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
