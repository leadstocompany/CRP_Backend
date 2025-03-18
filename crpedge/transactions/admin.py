from django.contrib import admin
from .models import (
    ForecastTemplate, ActualTemplate, Forecast, ForecastDetail,
    Actual, ActualDetail, CreditFacility
)


@admin.register(ForecastTemplate)
class ForecastTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for ForecastTemplate model."""

    list_display = ('company', 'name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company__name', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ActualTemplate)
class ActualTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for ActualTemplate model."""

    list_display = ('company', 'name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company__name', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')


class ForecastDetailInline(admin.TabularInline):
    """Inline admin for ForecastDetail model."""

    model = ForecastDetail
    extra = 0
    fields = ('gl_account', 'category', 'subcategory', 'transaction_date', 'amount')


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    """Admin configuration for Forecast model."""

    list_display = ('company', 'reference_number', 'forecast_date', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'forecast_date', 'created_at')
    search_fields = ('company__name', 'reference_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ForecastDetailInline]


class ActualDetailInline(admin.TabularInline):
    """Inline admin for ActualDetail model."""

    model = ActualDetail
    extra = 0
    fields = ('gl_account', 'category', 'subcategory', 'transaction_date', 'amount')


@admin.register(Actual)
class ActualAdmin(admin.ModelAdmin):
    """Admin configuration for Actual model."""

    list_display = ('company', 'reference_number', 'actual_date', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'actual_date', 'created_at')
    search_fields = ('company__name', 'reference_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ActualDetailInline]


@admin.register(CreditFacility)
class CreditFacilityAdmin(admin.ModelAdmin):
    """Admin configuration for CreditFacility model."""

    list_display = (
    'company', 'reference_number', 'facility_type', 'bank', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'facility_type', 'bank', 'created_at')
    search_fields = ('company__name', 'reference_number', 'bank__name')
    readonly_fields = ('created_at', 'updated_at')