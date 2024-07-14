# automations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EjecucionesViewSet, MetricaViewSet, BitacoraMetricaViewSet, DispositivosViewSet

router = DefaultRouter()
router.register(r'ejecuciones', EjecucionesViewSet)
router.register(r'metrica', MetricaViewSet)
router.register(r'bitacora-metrica', BitacoraMetricaViewSet)
router.register(r'dispositivos', DispositivosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
