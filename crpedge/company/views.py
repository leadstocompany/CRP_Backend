from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from requests import Session
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from .models import Company, ActiveSession
from .serializers import CompanyRegistrationSerializer, LoginSerializer
import pyotp
import qrcode
import io
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CompanyUser

User = get_user_model()

class RegisterCompanyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CompanyRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()

            # Send Activation Email
            user = User.objects.get(username=request.data['email'])
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"{settings.FRONTEND_URL}/activate/{uid}"

            subject = "Activate Your Company Account"
            message = render_to_string("emails/activation_email.html", {
                "user": user,
                "activation_link": activation_link
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({"message": "Registration successful. Check your email for activation."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            if not user.is_active:
                user.is_active = True
                user.save()

                # Activate the company
                company = Company.objects.filter(companyuser__user=user).first()
                if company:
                    company.is_active = True
                    company.save()

                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)

            return Response({"message": "Account already activated."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)
class GenerateQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        company_user = CompanyUser.objects.get(user=user)

        # Generate OTP Secret Key
        secret_key = company_user.generate_otp_secret()

        # Generate QR Code
        otp_uri = f"otpauth://totp/{user.email}?secret={secret_key}&issuer=CompanyApp"
        qr = qrcode.make(otp_uri)

        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(buffer.getvalue(), content_type="image/png")

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

            subject = "Reset Your Password"
            message = render_to_string("emails/reset_password_email.html", {"reset_link": reset_link})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class TrackUserSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_key = request.session.session_key
        ip_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")

        ActiveSession.objects.create(
            user=request.user,
            session_key=session_key,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return Response({"message": "Session tracked!"})
class ActiveSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ActiveSession.objects.filter(user=request.user, is_active=True)
        data = [
            {
                "ip_address": session.ip_address,
                "user_agent": session.user_agent,
                "login_time": session.login_time,
            }
            for session in sessions
        ]
        return Response({"active_sessions": data})
class LogoutSpecificSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_key = request.data.get("session_key")
        try:
            session = Session.objects.get(session_key=session_key)
            session.delete()
            ActiveSession.objects.filter(session_key=session_key).delete()
            return Response({"message": "Logged out from the selected device."}, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAllSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_session_key = request.session.session_key
        ActiveSession.objects.filter(user=request.user).exclude(session_key=current_session_key).delete()
        Session.objects.exclude(session_key=current_session_key).delete()

        return Response({"message": "Logged out from all other devices."}, status=status.HTTP_200_OK)