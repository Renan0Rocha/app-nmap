"""
URL Configuration for portscanner_web project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scanner.urls')),
    path('', include('scanner.urls_web')),
]
