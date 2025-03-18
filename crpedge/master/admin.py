
from import_export.admin import ExportMixin
from django import forms

from .base_admin import BaseInlineSaveMixin, BaseSaveMixin
from .models import *

from django.contrib import admin
from .models import GLChartOfAccount

admin.site.site_header = "Cash Resource Planning"
admin.site.site_title = "My Admin"
admin.site.index_title = "Welcome to My CRP Dashboard"

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('user', 'content_type', 'action_flag')
    search_fields = ('object_repr', 'user__username')
    ordering = ('-action_time',)

    actions = ['clear_recent_actions']

    @admin.action(description=_("Clear selected recent actions"))
    def clear_recent_actions(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully cleared {count} recent actions.")

class DocumentHistoryInline(admin.StackedInline):
    model = DocumentHistory
    extra = 0  # No empty extra fields by default
    readonly_fields = ("document_number", "action", "performed_by", "performed_date")
    can_delete = False  # Prevent deletion of history records

class DocumentTypeInline(BaseInlineSaveMixin, admin.StackedInline):
    model = DocType
    extra = 0
    fields = ("document_type_code", "document_type_name", "starting_document_number", "next_doc_number", "company", "created_by", "created_date", "modified_by", "modified_date")
    readonly_fields = ("created_by", "created_date", "modified_by", "modified_date")

@admin.register(DocType)
class DocTypeAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = (
        "document_type_code",
        "document_type_name",
        "starting_document_number",
        "next_doc_number",
        "company","edit_button","delete_button"
    )
    search_fields = ("document_type_code", "document_type_name", "company__company_name")
    list_filter = ("company",)
    readonly_fields = ("created_by", "created_date", "modified_by", "modified_date")

    fieldsets = (
        ("Basic Info", {
            "fields": ("document_type_code", "document_type_name", "starting_document_number", "company")
        }),
        ("System Fields", {
            "fields": ("next_doc_number", "created_by", "created_date", "modified_by", "modified_date")
        }),
    )

    actions = ["reset_next_doc_number"]
    inlines = [DocumentHistoryInline]


    @admin.action(description="Reset Next Doc Number to Starting Document Number")
    def reset_next_doc_number(self, request, queryset):
        for obj in queryset:
            obj.next_doc_number = obj.starting_document_number
            obj.save()
        self.message_user(request, "Next Document Number has been reset.")
#
# @admin.register(DocType)
# class DocTypeAdmin(ExportMixin, admin.ModelAdmin):
#     list_display = (
#     'document_type_code', 'document_type_name', 'starting_document_number', 'company', 'next_doc_number')
#     search_fields = ('document_type_code', 'document_type_name', 'company_code')
#     list_filter = ('company',)
#     readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')
#
#     fieldsets = (
#         ("Basic Info",
#          {"fields": ("document_type_code", "document_type_name", "starting_document_number", "company")}),
#         (
#         "System Fields", {"fields": ("next_doc_number", "created_by", "created_date", "modified_by", "modified_date")}),
#     )
#
#     actions = ["reset_next_doc_number"]
#
#     inlines = [DocumentHistoryInline]  # Inline Editing
#
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # On creation
#             obj.created_by = request.user
#         obj.modified_by = request.user
#
#         # Auto-increment `next_doc_number`
#         if obj.starting_document_number and obj.next_doc_number is None:
#             obj.next_doc_number = obj.starting_document_number + 1
#
#         super().save_model(request, obj, form, change)
#
#     @admin.action(description="Reset Next Doc Number to Starting Document Number")
#     def reset_next_doc_number(self, request, queryset):
#         for obj in queryset:
#             obj.next_doc_number = obj.starting_document_number
#             obj.save()
#         self.message_user(request, "Next Document Number has been reset.")
#
#
# class DocumentHistoryInline(admin.TabularInline):
#     model = DocumentHistory
#     extra = 1  # Number of empty forms to display
#     readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')  # Read-only fields
#     fields = ('history_code', 'history_name', 'created_by', 'created_date', 'modified_by', 'modified_date')  # Fields to show

class MainCategoryInline(BaseInlineSaveMixin, admin.StackedInline):
    model = MainCategory
    extra = 1
    fields = ("category_code", "category_name", "company", "remark")
@admin.register(MainCategory)
class MainCategoryAdmin(ExportMixin, BaseSaveMixin,admin.ModelAdmin):
    list_display = ('category_code', 'category_name', 'company', 'created_by', 'created_date', 'modified_by', 'modified_date',"edit_button","delete_button")
    search_fields = ('category_code', 'category_name', 'company')
    list_filter = ('company', 'created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date')

    fieldsets = (
        ("Category Information", {
            'fields': ('category_code', 'category_name', 'company', 'remark')
        }),
        ("System Information", {
            'fields': ('username', 'created_by', 'created_date', 'modified_by', 'modified_date'),
        }),
    )

class SubCategoryInline(BaseInlineSaveMixin, admin.StackedInline):
    model = SubCategory
    extra = 1
    readonly_fields = ('created_date', 'modified_date', 'created_by', 'modified_by', 'username')
    fields = (
        "sub_category_code", "sub_category_description", "within_category_code", "company",
        "username", "remark", "created_date", "modified_date", "created_by", "modified_by"
    )
@admin.register(SubCategory)
class SubCategoryAdmin(BaseSaveMixin,admin.ModelAdmin):
    """
    Admin panel configuration for SubCategory with validation.
    """
    list_display = (
    "sub_category_code", "sub_category_description", "within_category_code", "company", "created_date",
    "modified_date","edit_button","delete_button")
    search_fields = ("sub_category_code", "sub_category_description")
    list_filter = ("created_date", "modified_date")

class ProjectInline(BaseInlineSaveMixin,admin.StackedInline):  # or use admin.StackedInline
    model = Project
    extra = 1  # Defines how many empty inline forms should be shown
    readonly_fields = ('created_date', 'modified_date', 'cash_forecast', 'net_profit_loss')

    fieldsets = (
        ('Project Details', {
            'fields': ('project_code', 'project_name', 'company', 'username', 'remark')
        }),
        ('Estimated Costs', {
            'fields': (
                'est_billing', 'est_dir_labour', 'est_dir_materials',
                'est_dir_overheads', 'est_dir_noncash',
                'est_indir_labour', 'est_indir_materials',
                'est_indir_overheads', 'est_indir_noncash'
            )
        }),
        ('Financial Calculations (Auto-Generated)', {
            'fields': ('cash_forecast', 'net_profit_loss')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )
@admin.register(Project)
class ProjectAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ('project_code', 'project_name', 'company', 'cash_forecast', 'net_profit_loss', 'created_date',"edit_button","delete_button")
    search_fields = ('project_code', 'project_name', 'company')
    list_filter = ('created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date', 'cash_forecast', 'net_profit_loss')

    fieldsets = (
        ('Project Details', {
            'fields': ('project_code', 'project_name', 'company', 'username', 'remark')
        }),
        ('Estimated Costs', {
            'fields': (
                'est_billing', 'est_dir_labour', 'est_dir_materials',
                'est_dir_overheads', 'est_dir_noncash',
                'est_indir_labour', 'est_indir_materials',
                'est_indir_overheads', 'est_indir_noncash'
            )
        }),
        ('Financial Calculations (Auto-Generated)', {
            'fields': ('cash_forecast', 'net_profit_loss')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )
class PartyInline(BaseInlineSaveMixin,admin.StackedInline):  # or use admin.StackedInline for a vertical layout
    model = Partie
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
    fields = ('party_code', 'party_name', 'company', 'created_date', 'modified_date')

@admin.register(Partie)
class PartyAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ('party_code', 'party_name', 'company', 'created_date', 'modified_date',"edit_button","delete_button")
    search_fields = ('party_code', 'party_name', 'company')
    list_filter = ('created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date')


class GLChartOfAccountInline(BaseInlineSaveMixin,admin.StackedInline):
    model = GLChartOfAccount
    extra = 1  # Show one empty form initially
    readonly_fields = ('created_date', 'modified_date', 'created_by', 'modified_by', 'username')
    fields = ('gl_acct_code', 'gl_acct_name', 'company', 'created_date', 'modified_date', 'created_by', 'modified_by', 'username')

@admin.register(GLChartOfAccount)
class GLChartOfAccountAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ('gl_acct_code', 'gl_acct_name', 'company', 'created_date', 'modified_date',"edit_button","delete_button")
    search_fields = ('gl_acct_code', 'gl_acct_name', 'company')
    list_filter = ('created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date', 'created_by', 'modified_by', 'username')

class BankInline(BaseInlineSaveMixin,admin.StackedInline):
    model = Bank
    extra = 1
    fields = ("bank_code", "bank_name", "bank_swift_ifsc", "bank_country", "created_date", "modified_date", "created_by", "modified_by", "username")
    readonly_fields = ("created_date", "modified_date", "created_by", "modified_by", "username")


@admin.register(Bank)
class BankAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ("bank_code", "bank_name", "bank_country", "company","edit_button","delete_button")
    list_filter = ("company", "bank_country")
    search_fields = ("bank_code", "bank_name", "bank_country", "company__company_name")
    fieldsets = (
        ("Bank Information", {
            "fields": ("bank_code", "bank_name", "bank_swift_ifsc", "bank_country", "company")
        }),
        ("System Information", {
            "fields": ("username", "remark", "created_by", "created_date", "modified_by", "modified_date")
        }),
    )
    readonly_fields = ("created_by", "created_date", "modified_by", "modified_date")

class BankBranchInline(BaseInlineSaveMixin,admin.StackedInline):  # You can use StackedInline if you prefer
    model = BankBranch
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')


@admin.register(BankBranch)
class BankBranchAdmin(BaseSaveMixin, admin.ModelAdmin):
    list_display = (
        'branch_code', 'branch_name', 'bank', 'bank_country',
        'created_date', 'modified_date',"edit_button","delete_button"
    )
    search_fields = ('branch_code', 'branch_name', 'bank__bank_name', 'bank_country')
    list_filter = ('bank_country', 'created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date')

    fieldsets = (
        ('Branch Details', {
            'fields': ('bank', 'branch_code', 'branch_name', 'bank_swift_ifsc', 'bank_state', 'bank_country', 'company',
                       'username', 'remark')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )

    def s_no(self, obj):
        queryset = Bank.objects.all()
        return list(queryset).index(obj) + 1

    s_no.short_description = "S.No"


class CreditFacilityMasterInline(BaseInlineSaveMixin,admin.StackedInline):  # You can use StackedInline if preferred
    model = CreditFacilityMaster
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
@admin.register(CreditFacilityMaster)
class CreditFacilityMasterAdmin(BaseSaveMixin, admin.ModelAdmin):
    list_display = (
        'category_code', 'credit_facility_code', 'credit_facility_name',
        'company', 'created_date', 'modified_date',"edit_button","delete_button"
    )
    search_fields = ('credit_facility_code', 'credit_facility_name', 'category_code', 'company__name')
    list_filter = ('created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date')

    fieldsets = (
        ('Credit Facility Details', {
            'fields': ('category_code', 'credit_facility_code', 'credit_facility_name', 'company', 'username', 'remark')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )
class Filter1Inline(BaseInlineSaveMixin,admin.StackedInline):
    model = Filter1
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
    fields = (
        'filter_code', 'filter_description', 'filter_purpose', 'company',
        'username', 'remark', 'company', 'created_by', 'created_date',
        'modified_by', 'modified_date'
    )
@admin.register(Filter1)
class Filter1Admin(BaseSaveMixin, admin.ModelAdmin):
    list_display = ('filter_code', 'filter_description', 'filter_purpose', 'company', 'created_date', 'modified_date',"edit_button","delete_button")
    search_fields = ('filter_code', 'filter_description', 'filter_purpose', 'company')
    list_filter = ('filter_purpose', 'created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date')

    fieldsets = (
        ('Filter Details', {
            'fields': ('filter_code', 'filter_description', 'filter_purpose','company', 'username', 'remark')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )
class SubFilter1Inline(BaseInlineSaveMixin,admin.StackedInline):
    model = SubFilter1
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
@admin.register(SubFilter1)
class SubFilter1Admin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ('sub_filter_code', 'sub_filter_desc', 'filter1', 'created_date',"edit_button","delete_button")
    search_fields = ('sub_filter_code', 'sub_filter_desc')
    list_filter = ('filter1', 'created_date')
class Filter2Inline(BaseInlineSaveMixin,admin.StackedInline):
    model = Filter2
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
@admin.register(Filter2)
class Filter2Admin(BaseSaveMixin, admin.ModelAdmin):
    list_display = ('filter_code', 'filter_description', 'filter_broad_description', 'username', 'company', 'created_date', 'modified_date',"edit_button","delete_button")
    search_fields = ('filter_code', 'filter_description', 'filter_broad_description', 'username', 'company')
    list_filter = ('filter_broad_description', 'company', 'created_date')
    readonly_fields = ('created_date', 'modified_date')
# @admin.register(Filter2)
# class Filter2Admin(BaseSaveMixin,admin.ModelAdmin):
#     list_display = ('filter_code', 'filter_description', 'filter_broad_description', 'created_date')
#     search_fields = ('filter_code', 'filter_description', 'filter_broad_description')
#     list_filter = ('filter_broad_description', 'created_date')
class SubFilter2Inline(BaseInlineSaveMixin,admin.StackedInline):
    model = SubFilter1
    extra = 1  # Number of empty forms to display
    readonly_fields = ('created_date', 'modified_date')
@admin.register(SubFilter2)
class SubFilter2Admin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ('sub_filter_code', 'sub_filter_description', 'filter2', 'created_date',"edit_button","delete_button")
    search_fields = ('sub_filter_code', 'sub_filter_description')
    list_filter = ('filter2', 'created_date')

class CurrencyCodeInline(BaseInlineSaveMixin,admin.StackedInline):
    model = CurrencyCode
    extra = 1
    readonly_fields = ("created_date", "modified_date", "created_by", "modified_by")
@admin.register(CurrencyCode)
class CurrencyCodeAdmin(BaseSaveMixin,admin.ModelAdmin):
    list_display = ("curr_code", "curr_name", "company", "created_date", "modified_date","edit_button","delete_button")
    search_fields = ("curr_code", "curr_name")
    list_filter = ("company", "created_date")
    readonly_fields = ("created_date", "modified_date", "created_by", "modified_by")


class CurrencyRateInline(BaseInlineSaveMixin,admin.StackedInline):
    model = CurrencyRate
    extra = 1
    readonly_fields = ("created_date", "modified_date", "created_by", "modified_by")
    fieldsets = (
        ("Currency Rate Information", {
            "fields": ("currency_code", "exchange_rate", "exchange_rate_date", "company", "currency_enabled")
        }),
        ("System Fields", {
            "fields": ("created_date", "modified_date", "created_by", "modified_by")
        }),
    )
@admin.register(CurrencyRate)
class CurrencyRateAdmin(ExportMixin, BaseSaveMixin,admin.ModelAdmin):
    list_display = ("currency_code", "exchange_rate", "exchange_rate_date", "company", "currency_enabled", "created_date","edit_button","delete_button")
    search_fields = ("currency_code", "company")
    list_filter = ("currency_code", "exchange_rate_date", "company", "currency_enabled")
    readonly_fields = ("created_date", "modified_date", "created_by", "modified_by")

    fieldsets = (
        ("Currency Rate Information", {
            "fields": ("currency_code", "exchange_rate", "exchange_rate_date", "company", "currency_enabled")
        }),
        ("System Fields", {
            "fields": ("created_date", "modified_date", "created_by", "modified_by")
        }),
    )