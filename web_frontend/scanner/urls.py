from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para API REST
router = DefaultRouter()
router.register(r'scans', views.ScanJobViewSet)
router.register(r'history', views.ScanHistoryViewSet)

urlpatterns = [
    # API REST
    path('', include(router.urls)),
    
    # Endpoints adicionais
    path('statistics/', views.scan_statistics, name='scan_statistics'),
    path('quick-scan/', views.quick_scan, name='quick_scan'),
]
