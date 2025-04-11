from django.db import models
from django.contrib.auth import get_user_model
import pyotp

User = get_user_model()

class Company(models.Model):
    # Basic company information
    company_code = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=255)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_companies')  # Changed to support parent-child hierarchy
    currency_code = models.CharField(max_length=10)

    # Organization hierarchy and structure
    level = models.PositiveIntegerField(default=0)  # Added to define the hierarchy level (e.g., division, sub-level)
    hierarchy_path = models.TextField(blank=True, null=True)  # To store the full hierarchy path as a string

    # Master Data Permissions (added hierarchical permissions)
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

    # License and usage tracking
    number_of_licenses_purchased = models.PositiveIntegerField(default=0)
    number_of_licenses_used = models.PositiveIntegerField(default=0)
    concurrent_users_now = models.PositiveIntegerField(default=0)

    # Company address and contact
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

    def available_licenses(self):
        return self.number_of_licenses_purchased - self.number_of_licenses_used

    def __str__(self):
        return self.company_name


class CompanyUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),  # New role for better hierarchy
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    # 2FA Secret Key
    otp_secret_key = models.CharField(max_length=32, blank=True, null=True)

    def generate_otp_secret(self):
        if not self.otp_secret_key:
            self.otp_secret_key = pyotp.random_base32()
            self.save()
        return self.otp_secret_key

    def verify_otp(self, otp_code):
        totp = pyotp.TOTP(self.otp_secret_key)
        return totp.verify(otp_code)


class ActiveSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.ip_address} - {self.login_time}"
