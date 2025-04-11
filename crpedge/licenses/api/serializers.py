from rest_framework import serializers
from licenses.models import License, LicenseAssignment


# ======================================
# Full License Serializer
# ======================================
class LicenseSerializer(serializers.ModelSerializer):
    """
    Serializer for full License model data.
    Used for viewing or managing licenses through the API.
    Some fields like license_key, status, and created_at are read-only.
    """
    class Meta:
        model = License
        fields = '__all__'
        read_only_fields = ['license_key', 'status', 'created_at']


# ======================================
# Trial Request Serializer
# ======================================
class TrialRequestSerializer(serializers.Serializer):
    """
    Serializer for initiating a trial license.
    Client must explicitly confirm they want to start a trial.
    """
    confirm = serializers.BooleanField()

    def validate_confirm(self, value):
        """
        Ensure the user has actually confirmed the trial request.
        """
        if not value:
            raise serializers.ValidationError("You must confirm to start a trial.")
        return value


# ======================================
# License Activation Serializer
# ======================================
class LicenseActivateSerializer(serializers.Serializer):
    """
    Serializer used to activate a license using a license key.
    """
    license_key = serializers.CharField(max_length=20)
# ======================================
# License Assignment Serializer
# ======================================
# class LicenseAssignmentSerializer(serializers.ModelSerializer):
#     """
#     Serializer for assigning users to a license.
#     """
#     class Meta:
#         model = LicenseAssignment
#         fields = ['id', 'license', 'user', 'assigned_at']
#         read_only_fields = ['assigned_at']
class LicenseAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing license assignments.
    """
    class Meta:
        model = LicenseAssignment
        fields = '__all__'
        read_only_fields = ['assigned_at', 'license']