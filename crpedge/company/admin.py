
from django.contrib import admin
from django.utils.html import format_html

from .models import Company
from master.admin import *


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
            "fields": ("company_code", "company_name", "parent_code", "currency_code"),
        }),
        ("Features Access", {
            "fields": (
                ("document_types", "main_categories", "sub_categories", "projects"),
                ("parties", "gl_chart_of_accounts", "banks", "banks_branches"),
                ("credit_facility_master", "filter1", "sub_filter1", "filter2"),
                ("sub_filter2", "curr_codes", "curr_rates"),
            ),
            "classes": ("collapse",),  # Optional: Makes the section collapsible
        }),
        ("License Information", {
            "classes": ("collapse",),
            "fields": ("number_of_licenses_purchased", "number_of_licenses_used", "concurrent_users_now"),
        }),
    )

    def selected_features(self, obj):
        """Display selected features as a comma-separated list."""
        selected = []
        fields = [
            "document_types", "main_categories", "sub_categories", "projects",
            "parties", "gl_chart_of_accounts", "banks", "banks_branches",
            "credit_facility_master", "filter1", "sub_filter1", "filter2",
            "sub_filter2", "curr_codes", "curr_rates"
        ]
        for field in fields:
            if getattr(obj, field):
                selected.append(field.replace("_", " ").title())
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
            '<a href="{}" style="text-decoration: none; color: red; font-weight: bold;" onclick="return confirm(\'Are you sure you want to delete this item?\')">🗑️ Delete</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/delete/"
        )

    delete_button.short_description = "Delete"

    def select_all(self, request, queryset):
        self.message_user(request, f"All {queryset.count()} companies selected.")

    select_all.short_description = "Select All Companies"

    def get_inlines(self, request, obj=None):
        inlines = []

        if obj:
            if obj.banks:
                inlines.append(BankInline)
            if obj.document_types:
                inlines.append(DocumentTypeInline)
            if obj.gl_chart_of_accounts:
                inlines.append(GLChartOfAccountInline)
            if obj.main_categories:
                inlines.append(MainCategoryInline)
            if obj.sub_categories:
                inlines.append(SubCategoryInline)
            if obj.projects:
                inlines.append(ProjectInline)
            if obj.parties:
                inlines.append(PartyInline)
            if obj.banks_branches:
                inlines.append(BankBranchInline)
            if obj.credit_facility_master:
                inlines.append(CreditFacilityMasterInline)
            if obj.filter1:
                inlines.append(Filter1Inline)
            if obj.sub_filter1:
                inlines.append(SubFilter1Inline)
            if obj.filter2:
                inlines.append(Filter2Inline)
            if obj.sub_filter2:
                inlines.append(SubFilter2Inline)
            if obj.curr_codes:
                inlines.append(CurrencyCodeInline)
            if obj.curr_rates:
                inlines.append(CurrencyRateInline)

        return inlines

