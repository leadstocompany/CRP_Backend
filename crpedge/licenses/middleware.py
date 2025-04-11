from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from licenses.models import License


class LicenseValidationMiddleware(MiddlewareMixin):
    """
    Middleware to enforce active license validation for authenticated users.
    Allows requests only if the user has an active individual or company license.
    """

    def process_request(self, request):
        # Allow unauthenticated users (e.g., login, signup, public APIs)
        if not request.user.is_authenticated:
            return None

        # Allow access to Django admin
        if request.path.startswith('/admin/'):
            return None

        # Allow access for superusers and staff regardless of license
        if request.user.is_superuser or request.user.is_staff:
            return None

        user = request.user
        today = timezone.now().date()

        # Start with individual license check
        license_qs = License.objects.filter(
            license_type='individual',
            user=user,
            status='active',
            start_date__lte=today,
            end_date__gte=today
        )

        # If user belongs to a company, include active company license in query
        if hasattr(user, 'companyuser') and user.companyuser.company:
            license_qs = license_qs | License.objects.filter(
                license_type='company',
                company=user.companyuser.company,
                status='active',
                start_date__lte=today,
                end_date__gte=today
            )

        # Get first matched license
        license = license_qs.first()

        # No active license found — block access
        if not license:
            return JsonResponse(
                {'detail': 'Access denied. No active license found. Please renew your subscription.'},
                status=402
            )

        # License is valid — request continues
        return None
