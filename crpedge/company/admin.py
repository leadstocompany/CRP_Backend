import pyotp
from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django import forms

from .models import Company, CompanyUser
from master.admin import (
    BankInline, DocumentTypeInline, GLChartOfAccountInline, MainCategoryInline,
    SubCategoryInline, ProjectInline, PartyInline, BankBranchInline,
    CreditFacilityMasterInline, Filter1Inline, SubFilter1Inline, Filter2Inline,
    SubFilter2Inline, CurrencyCodeInline, CurrencyRateInline
)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company_code",
        "company_name",
        "created_date",
        "modified_date",
        "selected_features",  # Display selected features in the list view
        "edit_button",
        "delete_button",
    )
    list_filter = ("company_name", "created_date")
    search_fields = ("company_code", "company_name")

    fieldsets = (
        ("Company Information", {
            "classes": ("collapse",),
            "fields": ("company_code", "company_name", "parent_company", "currency_code"),
        }),
        ("Features Access", {
            "fields": (
                ("document_types", "main_categories", "sub_categories", "projects"),
                ("parties", "gl_chart_of_accounts", "banks", "banks_branches"),
                ("credit_facility_master", "filter1", "sub_filter1", "filter2"),
                ("sub_filter2", "curr_codes", "curr_rates"),
            ),
            "classes": ("collapse",),
        }),
        ("License Information", {
            "classes": ("collapse",),
            "fields": ("number_of_licenses_purchased", "number_of_licenses_used", "concurrent_users_now"),
        }),
    )

    def selected_features(self, obj):
        """
        Display selected features as a comma-separated list.
        Improved readability by using a list comprehension.
        """
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
        """
        Provides an edit link with a green pencil icon.
        """
        return format_html(
            '<a href="{}" style="text-decoration: none; color: green; font-weight: bold;">✏️ Edit</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/"
        )

    edit_button.short_description = "Edit"

    def delete_button(self, obj):
        """
        Provides a delete link with a red trash icon.
        """
        return format_html(
            '<a href="{}" style="text-decoration: none; color: red; font-weight: bold;" '
            'onclick="return confirm(\'Are you sure you want to delete this item?\')">🗑️ Delete</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/delete/"
        )

    delete_button.short_description = "Delete"

    def select_all(self, request, queryset):
        """
        Admin action to select all companies.
        """
        self.message_user(request, f"All {queryset.count()} companies selected.")

    select_all.short_description = "Select All Companies"

    def get_inlines(self, request, obj=None):
        """
        Dynamically display inlines based on the selected features.
        Improved readability and code structure.
        """
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

            # Dynamically add inlines based on selected features
            for feature, inline in inline_mapping.items():
                if getattr(obj, feature):
                    inlines.append(inline)

        return inlines


from django.contrib import admin
from django import forms
from django.utils.html import format_html
import pyotp
from .models import CompanyUser


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

        # Generate OTP secret key if it doesn't exist
        if not self.instance.otp_secret_key:
            self.instance.otp_secret_key = pyotp.random_base32()

        # Display the secret key in the form
        self.fields['otp_secret_key'].initial = self.instance.otp_secret_key

    def clean(self):
        cleaned_data = super().clean()
        otp_input = cleaned_data.get("otp_input")
        otp_secret_key = cleaned_data.get("otp_secret_key")

        if not otp_secret_key:
            raise forms.ValidationError("OTP secret key is missing. Please generate it first.")

        # Verify the OTP
        totp = pyotp.TOTP(otp_secret_key)
        if not totp.verify(otp_input):
            raise forms.ValidationError("Invalid OTP. Please try again.")

        return cleaned_data


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    form = CompanyUserForm
    list_display = ("user", "company", "role", "otp_secret_key")
    search_fields = ("user__username", "company__company_name")