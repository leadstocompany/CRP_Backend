"""
URL configuration for crpedge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# def redirect_to_admin(request):
#     return redirect('/admin/')

urlpatterns = [
    path('', lambda request: redirect('/admin/')),
    # path('', redirect_to_admin),  # Redirect root URL to admin
    path('admin/', admin.site.urls),
    path('api/master/', include('master.urls')),  # Your other API endpoints
    path('api/transactions/', include('transactions.urls')),
path('session-security/', include('session_security.urls')),  # ✅ Add this line


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)