# models.py
import random

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    mobile_number1 = models.CharField(max_length=15, blank=True, null=True)
    mobile_number2 = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    otp_via_email = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    entered_otp = models.CharField(max_length=6, blank=True, null=True)

    def generate_otp(self):
        """Generate a 6-digit OTP code."""
        return str(random.randint(100000, 999999))

    def send_otp_email(self):
        """Send OTP via email."""
        subject = "Your OTP Code"
        message = f"Your OTP code is: {self.otp_code}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.user.email])

    def save(self, *args, **kwargs):
        # Check if the OTP via email checkbox is selected
        if self.otp_via_email:
            # If OTP is already sent and entered OTP is present, verify it before saving
            if self.otp_code:
                if self.entered_otp and self.otp_code != self.entered_otp:
                    raise ValidationError("Entered OTP does not match the generated OTP.")
            else:
                # Generate and send OTP if not already sent
                self.otp_code = self.generate_otp()
                self.send_otp_email()
                print(f"OTP sent to {self.user.email}: {self.otp_code}")

        super().save(*args, **kwargs)