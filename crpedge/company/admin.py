from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from datetime import date

from .models import Company, CompanyUser
from licenses.models import License
from transactions.utils.forecasting import generate_cash_forecast
from django import forms
from django.utils.safestring import mark_safe
import pyotp
import qrcode
import base64
from io import BytesIO
from django.contrib import admin
from .models import CompanyUser

from master.admin import (
    BankInline, DocumentTypeInline, GLChartOfAccountInline, MainCategoryInline,
    SubCategoryInline, ProjectInline, PartyInline, BankBranchInline,
    CreditFacilityMasterInline, Filter1Inline, SubFilter1Inline, Filter2Inline,
    SubFilter2Inline, CurrencyCodeInline, CurrencyRateInline
)
# -------------------------------
# Inline for License inside Company
# -------------------------------
class LicenseInline(admin.TabularInline):
    model = License
    extra = 0
    readonly_fields = ['activated_on_display', 'expires_on_display', 'user_display']

    def activated_on_display(self, obj):
        return obj.start_date
    activated_on_display.short_description = "Activated On"

    def expires_on_display(self, obj):
        return obj.end_date
    expires_on_display.short_description = "Expires On"

    def user_display(self, obj):
        return obj.user.email if obj.user else "-"
    user_display.short_description = "User"

# -------------------------------
# Inline for CompanyUser inside Company
# -------------------------------
class CompanyUserInline(admin.TabularInline):
    model = CompanyUser
    extra = 0
    readonly_fields = ['otp_enabled']

    def otp_enabled(self, obj):
        return bool(obj.otp_secret_key)
    otp_enabled.boolean = True
    otp_enabled.short_description = '2FA Enabled'

# -------------------------------
# Main Company admin
# -------------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company_code",
        "company_name",
        "created_date",
        "modified_date",
        "selected_features",
        "edit_button",
        "delete_button",
    )
    list_filter = ("company_name", "created_date")
    search_fields = ("company_code", "company_name")

    readonly_fields = (
        "number_of_licenses_purchased",
        "number_of_licenses_used",
        "concurrent_users_now",
    )

    fieldsets = (
        ("Company Information", {
            "classes": ("collapse",),
            "fields": ("company_code", "company_name", "parent_company", "currency_code"),
        }),
        ("Features Access", {
            "classes": ("collapse",),
            "fields": (
                ("document_types", "main_categories", "sub_categories", "projects"),
                ("parties", "gl_chart_of_accounts", "banks", "banks_branches"),
                ("credit_facility_master", "filter1", "sub_filter1", "filter2"),
                ("sub_filter2", "curr_codes", "curr_rates"),
            ),
        }),
        ("License Information", {
            "classes": ("collapse",),
            "fields": (
                "number_of_licenses_purchased",
                "number_of_licenses_used",
                "concurrent_users_now",
            ),
        }),
    )

    def number_of_licenses_purchased(self, obj):
        """Total number of licenses (active + expired + trial) purchased for this company."""
        return License.objects.filter(company=obj).count()
    number_of_licenses_purchased.short_description = "Number of licenses purchased"

    def number_of_licenses_used(self, obj):
        """Number of currently active licenses (within valid date range)."""
        today = date.today()
        return License.objects.filter(company=obj, start_date__lte=today, end_date__gte=today).count()
    number_of_licenses_used.short_description = "Number of licenses used"

    def concurrent_users_now(self, obj):
        """Current number of concurrent users (tracked by middleware)."""
        return obj.current_users_count
    concurrent_users_now.short_description = "Concurrent users now"

    def selected_features(self, obj):
        fields = [
            "document_types", "main_categories", "sub_categories", "projects",
            "parties", "gl_chart_of_accounts", "banks", "banks_branches",
            "credit_facility_master", "filter1", "sub_filter1", "filter2",
            "sub_filter2", "curr_codes", "curr_rates"
        ]
        selected = [field.replace("_", " ").title() for field in fields if getattr(obj, field)]
        return ", ".join(selected) if selected else "-"
    selected_features.short_description = "Selected Features"

    def edit_button(self, obj):
        return format_html(
            '<a href="{}" style="text-decoration: none; color: green; font-weight: bold;">✏️ Edit</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/"
        )
    edit_button.short_description = "Edit"

    def delete_button(self, obj):
        return format_html(
            '<a href="{}" style="text-decoration: none; color: red; font-weight: bold;" '
            'onclick="return confirm(\'Are you sure you want to delete this item?\')">🗑️ Delete</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/delete/"
        )
    delete_button.short_description = "Delete"

    def select_all(self, request, queryset):
        self.message_user(request, f"All {queryset.count()} companies selected.")
    select_all.short_description = "Select All Companies"

    def get_inlines(self, request, obj=None):
        inlines = []

        if obj:
            inline_mapping = {
                'banks': BankInline,
                'document_types': DocumentTypeInline,
                'gl_chart_of_accounts': GLChartOfAccountInline,
                'main_categories': MainCategoryInline,
                'sub_categories': SubCategoryInline,
                'projects': ProjectInline,
                'parties': PartyInline,
                'banks_branches': BankBranchInline,
                'credit_facility_master': CreditFacilityMasterInline,
                'filter1': Filter1Inline,
                'sub_filter1': SubFilter1Inline,
                'filter2': Filter2Inline,
                'sub_filter2': SubFilter2Inline,
                'curr_codes': CurrencyCodeInline,
                'curr_rates': CurrencyRateInline,
            }

            for feature, inline in inline_mapping.items():
                if getattr(obj, feature):
                    inlines.append(inline)

        return inlines



class CompanyUserForm(forms.ModelForm):
    otp_secret_key = forms.CharField(
        label="OTP Secret Key",
        max_length=50,
        required=False,
        help_text="The secret key to configure your authenticator app."
    )
    otp_input = forms.CharField(
        label="Enter OTP",
        max_length=6,
        required=True,
        help_text="Please enter the OTP generated by your authenticator app."
    )

    class Meta:
        model = CompanyUser
        fields = ["user", "company", "role", "otp_secret_key", "otp_input"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate new OTP secret key if not already set
        if not self.instance.otp_secret_key:
            self.instance.otp_secret_key = pyotp.random_base32()

        otp_secret_key = self.instance.otp_secret_key
        self.fields["otp_secret_key"].initial = otp_secret_key

        # Generate QR code for OTP
        username = self.instance.user.username if self.instance.user_id else "new_user"
        totp = pyotp.TOTP(otp_secret_key)
        uri = totp.provisioning_uri(name=username, issuer_name="CRP Dashboard")
        qr = qrcode.make(uri)
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Embed QR code in help text
        qr_html = f'<br><img src="data:image/png;base64,{img_base64}" height="180" /><br>'
        qr_html += f'<small>Scan this QR code in your Authenticator App</small>'

        self.fields["otp_secret_key"].help_text = mark_safe(
            f"The secret key to configure your authenticator app.<br><b>{otp_secret_key}</b>{qr_html}"
        )

    def clean(self):
        cleaned_data = super().clean()
        otp_input = cleaned_data.get("otp_input")
        otp_secret_key = cleaned_data.get("otp_secret_key")

        if not otp_secret_key:
            raise forms.ValidationError("OTP secret key is missing. Please generate it first.")

        # Verify the OTP entered by user
        totp = pyotp.TOTP(otp_secret_key)
        if not totp.verify(otp_input):
            raise forms.ValidationError("Invalid OTP. Please try again.")

        return cleaned_data


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    form = CompanyUserForm
    list_display = ("user", "company", "role")
    search_fields = ("user__username", "company__company_name")