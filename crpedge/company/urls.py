from django.urls import path
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("generate-qr/", GenerateQRCodeView.as_view(), name="generate-qr"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("track-session/", TrackUserSessionView.as_view(), name="track-session"),
    path("active-sessions/", ActiveSessionsView.as_view(), name="active-sessions"),
    path("logout-device/", LogoutSpecificSessionView.as_view(), name="logout-device"),
    path("logout-all/", LogoutAllSessionsView.as_view(), name="logout-all"),
]