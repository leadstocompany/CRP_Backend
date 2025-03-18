from django.db import models
import uuid

from company.models import Company
from master.models import CurrencyRate, GLChartOfAccount, MainCategory


# from companies.models import Company, CompanyUser
from master.models import *


class ForecastTemplate(models.Model):
    """Model for forecast templates."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='forecast_templates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='created_forecast_templates',
                                   null=True)
    updated_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='updated_forecast_templates',
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Forecast Templates'
        ordering = ['company', 'name']

    def __str__(self):
        return f"{self.company.company_name} - {self.name}"


class ActualTemplate(models.Model):
    """Model for actual templates."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='actual_templates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='created_actual_templates',
                                   null=True)
    updated_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='updated_actual_templates',
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Actual Templates'
        ordering = ['company', 'name']

    def __str__(self):
        return f"{self.company.company_name} - {self.name}"


class Forecast(models.Model):
    """Model for forecasts."""

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='forecasts')
    template = models.ForeignKey(ForecastTemplate, on_delete=models.PROTECT, related_name='forecasts')
    reference_number = models.CharField(max_length=50, unique=True)
    forecast_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.ForeignKey(CurrencyRate, on_delete=models.PROTECT, related_name='forecasts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='created_forecasts')
    updated_by = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='updated_forecasts')
    approved_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='approved_forecasts',
                                    null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Forecasts'
        ordering = ['-forecast_date']

    def __str__(self):
        return f"{self.company.company_name} - {self.reference_number} ({self.forecast_date})"


class ForecastDetail(models.Model):
    """Model for forecast details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE, related_name='details')
    gl_account = models.ForeignKey(GLChartOfAccount, on_delete=models.PROTECT, related_name='forecast_details')
    category = models.ForeignKey(MainCategory, on_delete=models.PROTECT, related_name='forecast_details')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='forecast_details', null=True,
                                    blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='forecast_details', null=True,
                                blank=True)
    party = models.ForeignKey(Partie, on_delete=models.PROTECT, related_name='forecast_details', null=True, blank=True)
    filter1 = models.ForeignKey(Filter1, on_delete=models.PROTECT, related_name='forecast_details_filter1', null=True,
                                blank=True)
    subfilter1 = models.ForeignKey(SubFilter1, on_delete=models.PROTECT, related_name='forecast_details_subfilter1',
                                   null=True, blank=True)
    filter2 = models.ForeignKey(Filter2, on_delete=models.PROTECT, related_name='forecast_details_filter2', null=True,
                                blank=True)
    subfilter2 = models.ForeignKey(SubFilter2, on_delete=models.PROTECT, related_name='forecast_details_subfilter2',
                                   null=True, blank=True)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Forecast Details'
        ordering = ['forecast', 'transaction_date']

    def __str__(self):
        return f"{self.forecast.reference_number} - {self.gl_account.name} - {self.amount}"


class Actual(models.Model):
    """Model for actuals."""

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='actuals')
    template = models.ForeignKey(ActualTemplate, on_delete=models.PROTECT, related_name='actuals')
    reference_number = models.CharField(max_length=50, unique=True)
    actual_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.ForeignKey(CurrencyRate, on_delete=models.PROTECT, related_name='actuals')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='created_actuals')
    updated_by = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='updated_actuals')
    approved_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='approved_actuals', null=True,
                                    blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Actuals'
        ordering = ['-actual_date']

    def __str__(self):
        return f"{self.company.company_name} - {self.reference_number} ({self.actual_date})"


class ActualDetail(models.Model):
    """Model for actual details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actual = models.ForeignKey(Actual, on_delete=models.CASCADE, related_name='details')
    gl_account = models.ForeignKey(GLChartOfAccount, on_delete=models.PROTECT, related_name='actual_details')
    category = models.ForeignKey(MainCategory, on_delete=models.PROTECT, related_name='actual_details')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='actual_details', null=True,
                                    blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='actual_details', null=True, blank=True)
    party = models.ForeignKey(Partie, on_delete=models.PROTECT, related_name='actual_details', null=True, blank=True)
    filter1 = models.ForeignKey(Filter1, on_delete=models.PROTECT, related_name='actual_details_filter1', null=True,
                                blank=True)
    subfilter1 = models.ForeignKey(SubFilter1, on_delete=models.PROTECT, related_name='actual_details_subfilter1',
                                   null=True, blank=True)
    filter2 = models.ForeignKey(Filter2, on_delete=models.PROTECT, related_name='actual_details_filter2', null=True,
                                blank=True)
    subfilter2 = models.ForeignKey(SubFilter2, on_delete=models.PROTECT, related_name='actual_details_subfilter2',
                                   null=True, blank=True)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Actual Details'
        ordering = ['actual', 'transaction_date']

    def __str__(self):
        return f"{self.actual.reference_number} - {self.gl_account.name} - {self.amount}"


class CreditFacility(models.Model):
    """Model for credit facilities."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='credit_facilities')
    reference_number = models.CharField(max_length=50, unique=True)
    facility_type = models.ForeignKey('master.CreditFacilityMaster', on_delete=models.PROTECT, related_name='facilities')
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='credit_facilities')
    bank_branch = models.ForeignKey(BankBranch, on_delete=models.PROTECT, related_name='credit_facilities')
    currency = models.ForeignKey(CurrencyRate, on_delete=models.PROTECT, related_name='credit_facilities')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='created_credit_facilities')
    approved_by = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='approved_credit_facilities',
                                    null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Credit Facilities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.company_name} - {self.reference_number} - {self.facility_type.name}"