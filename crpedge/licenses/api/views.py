from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from company.models import CompanyUser
from licenses.services import SubscriptionService
from licenses.exceptions import LicenseError
from .serializers import (
    TrialRequestSerializer,
    LicenseSerializer,
    LicenseActivateSerializer, LicenseAssignmentSerializer
)
from .. import serializers
from ..models import LicenseAssignment


class TrialLicenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TrialRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            company_user = CompanyUser.objects.get(user=request.user)
        except CompanyUser.DoesNotExist:
            return Response({"error": "You are not associated with any company."}, status=status.HTTP_400_BAD_REQUEST)

        service = SubscriptionService(company_user)

        try:
            license = service.create_trial_license()
            return Response(LicenseSerializer(license).data, status=status.HTTP_201_CREATED)
        except LicenseError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ActivateLicenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LicenseActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            company_user = CompanyUser.objects.get(user=request.user)
        except CompanyUser.DoesNotExist:
            return Response({"error": "You are not associated with any company."}, status=status.HTTP_400_BAD_REQUEST)

        service = SubscriptionService(company_user)

        try:
            license = service.activate_license(serializer.validated_data['license_key'])
            return Response(LicenseSerializer(license).data)
        except LicenseError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ActiveLicenseStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            company_user = CompanyUser.objects.get(user=request.user)
        except CompanyUser.DoesNotExist:
            return Response({"error": "You are not associated with any company."}, status=status.HTTP_400_BAD_REQUEST)

        service = SubscriptionService(company_user)
        license = service.get_active_license()

        if license:
            return Response(LicenseSerializer(license).data)
        return Response({"detail": "No active license."}, status=status.HTTP_404_NOT_FOUND)


class LicenseRenewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            company_user = CompanyUser.objects.get(user=request.user)
        except CompanyUser.DoesNotExist:
            return Response({"error": "You are not associated with any company."}, status=status.HTTP_400_BAD_REQUEST)

        service = SubscriptionService(company_user)

        try:
            renewed_license = service.renew_license()
            return Response({
                "message": "License renewed successfully.",
                "license": LicenseSerializer(renewed_license).data
            })
        except LicenseError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class LicenseAssignmentListCreateView(ListCreateAPIView):
    """
    GET /api/licenses/assignments/
    POST /api/licenses/assignments/

    - Lists all user assignments for the current active license of the company.
    - Allows creating a new license assignment (assigning a user to a license).

    Permissions:
        - Only authenticated users can access.
        - The user's company must have an active license.
    """
    serializer_class = LicenseAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return license assignments for the current company’s active license only.
        """
        company_user = self.request.user.companyuser
        active_license = company_user.company.licenses.filter(status='active').first()
        return LicenseAssignment.objects.filter(license=active_license)

    def perform_create(self, serializer):
        """
        Assign a user to a license. The license is auto-determined from the
        requesting user's company active license.
        """
        company_user = self.request.user.companyuser
        active_license = company_user.company.licenses.filter(status='active').first()

        if not active_license:
            raise serializers.ValidationError("No active license available for assignment.")

        serializer.save(license=active_license)
