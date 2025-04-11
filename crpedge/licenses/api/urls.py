from django.urls import path
from .views import (
    TrialLicenseView,
    ActivateLicenseView,
    ActiveLicenseStatusView,
    LicenseRenewView,
    LicenseAssignmentListCreateView,  # Optional - for managing license assignments
)

urlpatterns = [
    # -------------------------------------------------------------------------
    # POST /api/licenses/trial/
    # Initiates a trial license for the authenticated user or company.
    # Requires explicit confirmation input from the client.
    # -------------------------------------------------------------------------
    path('trial/', TrialLicenseView.as_view(), name='license-trial'),

    # -------------------------------------------------------------------------
    # POST /api/licenses/activate/
    # Activates a license using a valid license key provided by the client.
    # Typically used for license key redemption.
    # -------------------------------------------------------------------------
    path('activate/', ActivateLicenseView.as_view(), name='license-activate'),

    # -------------------------------------------------------------------------
    # GET /api/licenses/status/
    # Returns the active license status (valid, expired, etc.) for the
    # authenticated user or their associated company.
    # -------------------------------------------------------------------------
    path('status/', ActiveLicenseStatusView.as_view(), name='license-status'),

    # -------------------------------------------------------------------------
    # POST /api/licenses/license/renew/
    # Handles renewal logic for an existing paid license.
    # Can extend validity based on business rules (e.g., 1 year).
    # -------------------------------------------------------------------------
    path('license/renew/', LicenseRenewView.as_view(), name='license-renew'),

    # -------------------------------------------------------------------------
    # GET/POST /api/licenses/assign/
    # [GET]  - Lists license assignments (admin only).
    # [POST] - Assigns a license to a user (typically by a company admin).
    # Helps enforce concurrent user limits per license.
    # -------------------------------------------------------------------------
    path('assign/', LicenseAssignmentListCreateView.as_view(), name='license-assign'),
]
