from django.urls import path
from . import views

app_name = 'scanner_web'

from . import views_simple

urlpatterns = [
    # Interface Web
    path('', views.index, name='index'),
    path('job/<uuid:job_id>/', views.job_detail, name='job_detail'),
    
    # API Simples
    path('api/simple-scan/', views_simple.simple_scan, name='simple_scan'),
]
