from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from .models import License, LicenseAssignment
from .exceptions import LicenseError
from .utils import generate_license_key


class SubscriptionService:
    def __init__(self, *, company=None, user=None):
        """
        Initialize the service with either a company or individual user.
        """
        self.company = company
        self.user = user

        if not company and not user:
            raise LicenseError("Either 'company' or 'user' must be provided.")

    def _get_filter_kwargs(self):
        """
        Build filter kwargs based on whether this is a company or individual license.
        Used for filtering licenses.
        """
        if self.company:
            return {'company': self.company, 'license_type': 'company'}
        return {'user': self.user, 'license_type': 'individual'}

    def create_trial_license(self):
        """
        Create a trial license valid for 14 days.
        Raises error if a trial has already been used by this entity.
        """
        filter_kwargs = self._get_filter_kwargs()

        # Prevent multiple trials
        if License.objects.filter(**filter_kwargs, is_trial=True).exists():
            raise LicenseError("Trial license already used.")

        today = timezone.now().date()
        trial_end = today + timedelta(days=14)

        # Create and return trial license
        return License.objects.create(
            **filter_kwargs,
            license_key=generate_license_key(),
            is_trial=True,
            is_paid=False,
            start_date=today,
            end_date=trial_end,
            status='active'
        )

    def activate_license(self, license_key: str):
        """
        Validate and activate a license using the license key.
        Ensures the license exists, is active, and not expired.
        """
        filter_kwargs = self._get_filter_kwargs()

        try:
            license = License.objects.get(license_key=license_key, **filter_kwargs)
        except License.DoesNotExist:
            raise LicenseError("Invalid license key or unauthorized access.")

        if license.status != 'active':
            raise LicenseError(f"License is not active. Status: {license.status}")

        if license.end_date < timezone.now().date():
            raise LicenseError("License has already expired.")

        return license

    def get_active_license(self):
        """
        Retrieve the currently active license (trial or paid).
        Only returns a license valid for the current date range.
        """
        filter_kwargs = self._get_filter_kwargs()
        today = timezone.now().date()

        return License.objects.filter(
            **filter_kwargs,
            status='active',
            start_date__lte=today,
            end_date__gte=today
        ).first()

    @transaction.atomic
    def generate_paid_license(self):
        """
        Create a new paid license valid for 1 year.
        Expires any existing active licenses for the same entity.
        """
        filter_kwargs = self._get_filter_kwargs()

        # Expire currently active licenses before issuing a new one
        License.objects.filter(**filter_kwargs, status='active').update(status='expired')

        today = timezone.now().date()
        end_date = today + timedelta(days=365)

        # Create new paid license
        new_license = License.objects.create(
            **filter_kwargs,
            license_key=generate_license_key(),
            is_trial=False,
            is_paid=True,
            start_date=today,
            end_date=end_date,
            status='active'
        )
        return new_license

    def renew_license(self):
        """
        Renew the latest active license by extending its end date by 1 year.
        Useful for paid license extensions.
        """
        filter_kwargs = self._get_filter_kwargs()

        # Get the most recent active license
        current_license = License.objects.filter(
            **filter_kwargs,
            status='active'
        ).order_by('-end_date').first()

        if not current_license:
            raise LicenseError("No active license found to renew.")

        # Extend end date and regenerate license key
        current_license.end_date += timedelta(days=365)
        current_license.license_key = generate_license_key()
        current_license.is_trial = False
        current_license.is_paid = True
        current_license.save()

        return current_license

    def assign_user(self, user):
        """
        Assigns the user to the currently active license.
        Raises an error if license is full.
        """
        license = self.get_active_license()
        if not license:
            raise LicenseError("No active license available.")

        if license.current_users_count >= license.max_users_allowed:
            raise LicenseError("User limit reached for this license.")

        # Prevent duplicate assignment
        if LicenseAssignment.objects.filter(license=license, user=user).exists():
            return license

        LicenseAssignment.objects.create(license=license, user=user)
        license.current_users_count += 1
        license.save()
        return license

    def release_user(self, user):
        """
        Releases the user's license assignment and decrements usage count.
        """
        assignment = LicenseAssignment.objects.filter(user=user).select_related('license').first()
        if assignment:
            license = assignment.license
            assignment.delete()
            license.current_users_count = max(0, license.current_users_count - 1)
            license.save()
