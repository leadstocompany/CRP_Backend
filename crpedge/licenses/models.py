from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import secrets

# Get the custom or default User model
User = get_user_model()


class License(models.Model):
    """
    Represents a license record issued to either a company or an individual user.
    Can be a paid or trial license with a validity period and status tracking.
    """

    LICENSE_TYPE_CHOICES = [
        ('company', 'Company'),
        ('individual', 'Individual'),
    ]

    LICENSE_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    license_key = models.CharField(max_length=20, unique=True, editable=False)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPE_CHOICES)

    # Linked company (if license_type is 'company')
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='licenses',
        help_text="Required if license_type is 'company'"
    )

    # Linked user (if license_type is 'individual')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Required if license_type is 'individual'"
    )

    is_trial = models.BooleanField(default=False)  # True if trial license
    is_paid = models.BooleanField(default=False)   # True if paid license

    status = models.CharField(max_length=20, choices=LICENSE_STATUS, default='active')

    start_date = models.DateField()
    end_date = models.DateField()

    # Tracks how many users are concurrently using this license
    current_users_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    max_users_allowed = models.PositiveIntegerField(default=1)

    def clean(self):
        """
        Validate that either is_trial or is_paid is True (but not both),
        and that the correct license target (company/user) is set.
        """
        if self.is_trial and self.is_paid:
            raise ValidationError("A license cannot be both trial and paid.")
        if not self.is_trial and not self.is_paid:
            raise ValidationError("A license must be either trial or paid.")
        if self.license_type == 'company' and not self.company:
            raise ValidationError("Company must be set for a company license.")
        if self.license_type == 'individual' and not self.user:
            raise ValidationError("User must be set for an individual license.")

    def save(self, *args, **kwargs):
        """
        Generate a license key if missing and run full validation before saving.
        """
        if not self.license_key:
            self.license_key = secrets.token_urlsafe(12).upper()[:12]

        self.full_clean()  # Trigger clean() before save
        super().save(*args, **kwargs)

    def is_valid(self):
        """
        Check if license is active and not expired.
        """
        return self.status == 'active' and self.end_date >= timezone.now().date()

    @property
    def is_expired(self):
        """
        Returns True if the license has expired.
        """
        return self.end_date < timezone.now().date()

    def __str__(self):
        """
        Display license key, type, and assigned target (company/user).
        """
        target = (
            self.company.company_name
            if self.license_type == 'company' and self.company
            else self.user.username if self.user
            else "Unknown"
        )
        return f"{self.license_key} ({'Trial' if self.is_trial else 'Paid'}) → {target}"


class LicenseAssignment(models.Model):
    """
    Represents assignment of a license to an individual user.
    Used for company licenses to track which users are consuming license seats.
    """

    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp of assignment

    class Meta:
        unique_together = ('license', 'user')  # Prevent duplicate assignments
        verbose_name = "License Assignment"
        verbose_name_plural = "License Assignments"

    def __str__(self):
        return f"{self.user.username} → {self.license.license_key}"
