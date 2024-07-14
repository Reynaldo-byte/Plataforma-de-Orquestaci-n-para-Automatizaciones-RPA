# automations/models.py
from django.db import models

class Memoria(models.Model):
    capacidad = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainapp_memoria'

class SsdCapacidad(models.Model):
    capacidad = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainapp_ssdcapacidad'

class Resolucion(models.Model):
    resolucion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainapp_resolucion'

class SistemaOperativo(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainapp_sistemaoperativo'

class Dispositivos(models.Model):
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    memoria_ram = models.ForeignKey(Memoria, on_delete=models.CASCADE)
    ssd = models.ForeignKey(SsdCapacidad, on_delete=models.CASCADE)
    resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE)
    so = models.ForeignKey(SistemaOperativo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'mainapp_dispositivos'

class Catalogo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'mainapp_catalogo'

class Metrica(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'mainapp_metrica'

class Ejecuciones(models.Model):
    nombre = models.CharField(max_length=255)
    timestamp_inicio = models.DateTimeField()
    timestamp_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50)
    dispositivo = models.ForeignKey(Dispositivos, on_delete=models.CASCADE)
    automatizacion = models.ForeignKey(Catalogo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'mainapp_ejecuciones'

class BitacoraMetrica(models.Model):
    ejecucion = models.ForeignKey(Ejecuciones, on_delete=models.CASCADE)
    metrica_id = models.IntegerField()
    valor = models.FloatField()
    FechaRegistro = models.DateField()
    HoraRegistro = models.TimeField()

    class Meta:
        managed = False
        db_table = 'mainapp_bitacorametrica'
