from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Create a User object but do not save it to the database
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # Create a UserProfile and send OTP
        user_profile = UserProfile.objects.create(user=user, otp_via_email=True)
        user_profile.save()

        return render(request, "enter_otp.html", {"user_id": user.id})
    return render(request, "register.html")


def verify_otp(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        entered_otp = request.POST.get("otp")

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            if user_profile.verify_otp(entered_otp):
                return redirect("login")
            else:
                return render(request, "enter_otp.html", {"error": "Invalid OTP"})
        except UserProfile.DoesNotExist:
            return render(request, "enter_otp.html", {"error": "User not found"})

    return render(request, "enter_otp.html")
