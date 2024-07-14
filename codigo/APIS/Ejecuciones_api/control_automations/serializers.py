# automations/serializers.py
from rest_framework import serializers
from .models import Ejecuciones, Metrica, BitacoraMetrica, Dispositivos

class DispositivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivos
        fields = '__all__'

class EjecucionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejecuciones
        fields = '__all__'

class MetricaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrica
        fields = '__all__'

class BitacoraMetricaSerializer(serializers.ModelSerializer):
    metrica_nombre = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = BitacoraMetrica
        fields = ['ejecucion', 'metrica_id', 'valor', 'FechaRegistro', 'HoraRegistro', 'metrica_nombre']

    def create(self, validated_data):
        metrica_nombre = validated_data.pop('metrica_nombre', None)
        if metrica_nombre:
            metrica, created = Metrica.objects.get_or_create(nombre=metrica_nombre)
            validated_data['metrica_id'] = metrica.id
        return super().create(validated_data)