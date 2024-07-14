# mainapp/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Dispositivos(models.Model):
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    memoria_ram = models.ForeignKey('Memoria', on_delete=models.CASCADE)
    ssd = models.ForeignKey('SsdCapacidad', on_delete=models.CASCADE)
    resolucion = models.ForeignKey('Resolucion', on_delete=models.CASCADE)
    so = models.ForeignKey('SistemaOperativo', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre 


class Metrica(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
class SistemaOperativo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class SsdCapacidad(models.Model):
    capacidad = models.CharField(max_length=50)

    def __str__(self):
        return self.capacidad

class Memoria(models.Model):
    capacidad = models.CharField(max_length=50)

    def __str__(self):
        return self.capacidad

class Resolucion(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion


        

class Catalogo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    version = models.CharField(max_length=50)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre 

class Ejecuciones(models.Model):
    nombre = models.CharField(max_length=255)
    timestamp_inicio = models.DateTimeField()
    timestamp_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50)
    dispositivo = models.ForeignKey(Dispositivos, on_delete=models.CASCADE)  # Campo dispositivo obligatorio
    automatizacion = models.ForeignKey('Catalogo', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class BitacoraMetrica(models.Model):
    ejecucion = models.ForeignKey(Ejecuciones, on_delete=models.CASCADE)
    metrica_id = models.IntegerField()
    valor = models.FloatField()
    FechaRegistro = models.DateField()
    HoraRegistro = models.TimeField()

class Calendario(models.Model):
    automatizacion = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    hora_programada = models.TimeField()

class Ambientes(models.Model):
    nombre_ambiente = models.CharField(max_length=255)
    descripcion = models.TextField()

