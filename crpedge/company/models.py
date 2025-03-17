from django.db import models
from django.contrib.auth import get_user_model


class Company(models.Model):
    company_code = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=255)
    parent_code = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=10)

    document_types = models.BooleanField(default=False)
    main_categories = models.BooleanField(default=False)
    sub_categories = models.BooleanField(default=False)
    projects = models.BooleanField(default=False)
    parties = models.BooleanField(default=False)
    gl_chart_of_accounts = models.BooleanField(default=False)
    banks = models.BooleanField(default=False)
    banks_branches = models.BooleanField(default=False)
    credit_facility_master = models.BooleanField(default=False)
    filter1 = models.BooleanField(default=False)
    sub_filter1 = models.BooleanField(default=False)
    filter2 = models.BooleanField(default=False)
    sub_filter2 = models.BooleanField(default=False)
    curr_codes = models.BooleanField(default=False)
    curr_rates = models.BooleanField(default=False)

    number_of_licenses_purchased = models.PositiveIntegerField(default=0)
    number_of_licenses_used = models.PositiveIntegerField(default=0)
    concurrent_users_now = models.PositiveIntegerField(default=0)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=150)
    remark = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=150)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


