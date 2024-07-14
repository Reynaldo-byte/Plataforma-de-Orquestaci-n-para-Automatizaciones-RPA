# automations/views.py
from rest_framework import viewsets
from .models import Ejecuciones, Metrica, BitacoraMetrica, Dispositivos, Catalogo
from .serializers import EjecucionesSerializer, MetricaSerializer, BitacoraMetricaSerializer, DispositivosSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

class EjecucionesViewSet(viewsets.ModelViewSet):
    queryset = Ejecuciones.objects.all()
    serializer_class = EjecucionesSerializer

    def create(self, request, *args, **kwargs):
        dispositivo_nombre = request.data.get('dispositivo_nombre')
        automatizacion_nombre = request.data.get('automatizacion_nombre')
        try:
            dispositivo = Dispositivos.objects.get(nombre=dispositivo_nombre)
            if dispositivo.estado != 'Disponible':
                return Response({"error": "Dispositivo no autorizado"}, status=400)
        except Dispositivos.DoesNotExist:
            return Response({"error": "Dispositivo no encontrado"}, status=404)
        
        try:
            automatizacion = Catalogo.objects.get(nombre=automatizacion_nombre)
        except Catalogo.DoesNotExist:
            return Response({"error": "Automatización no encontrada"}, status=404)
        
        request.data['dispositivo'] = dispositivo.id
        request.data['automatizacion'] = automatizacion.id
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def end_execution(self, request, pk=None):
        ejecucion = self.get_object()
        ejecucion.timestamp_fin = timezone.now()
        ejecucion.estado = request.data.get('estado', 'completed')
        ejecucion.save()
        return Response(EjecucionesSerializer(ejecucion).data)

class MetricaViewSet(viewsets.ModelViewSet):
    queryset = Metrica.objects.all()
    serializer_class = MetricaSerializer

class BitacoraMetricaViewSet(viewsets.ModelViewSet):
    queryset = BitacoraMetrica.objects.all()
    serializer_class = BitacoraMetricaSerializer

class DispositivosViewSet(viewsets.ModelViewSet):
    queryset = Dispositivos.objects.all()
    serializer_class = DispositivosSerializer
