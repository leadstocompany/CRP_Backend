from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Company, CompanyUser

User = get_user_model()

class CompanyRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    number_of_licenses_purchased = serializers.IntegerField(min_value=1)

    class Meta:
        model = Company
        fields = ['company_name', 'company_code', 'currency_code', 'email', 'password', 'number_of_licenses_purchased']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # Create User (Company Admin)
        user = User.objects.create(username=email, email=email)
        user.set_password(password)
        user.is_active = False  # Require activation
        user.save()

        # Create Company
        company = Company.objects.create(**validated_data)

        # Assign User as Company Admin
        CompanyUser.objects.create(user=user, company=company, role='admin')

        # Send Activation Email (handled in views.py)
        return company
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    otp_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        otp_code = data.get("otp_code")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        company_user = CompanyUser.objects.get(user=user)
        if company_user.otp_secret_key:  # Check if 2FA is enabled
            if not otp_code:
                raise serializers.ValidationError("OTP code required.")
            if not company_user.verify_otp(otp_code):
                raise serializers.ValidationError("Invalid OTP code.")

        return {"user": user}