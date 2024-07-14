from django.test import TestCase, Client
from django.urls import reverse
from .models import Automatizacion, Ejecucion, Usuario

class AutomatizacionTests(TestCase):

    def setUp(self):
        # Configurar datos de prueba
        self.usuario = Usuario.objects.create(nombre="Test User", correo="test@example.com")
        self.automatizacion = Automatizacion.objects.create(
            nombre="Test Automation",
            descripcion="Descripción de prueba",
            version="1.0",
            autor=self.usuario
        )
        self.ejecucion = Ejecucion.objects.create(
            automatizacion=self.automatizacion,
            timestamp_inicio="2023-01-01 10:00:00",
            timestamp_fin="2023-01-01 11:00:00",
            estado="Completado"
        )
        self.client = Client()

    def test_automatizacion_creation(self):
        # Prueba de creación de automatización
        automatizacion = Automatizacion.objects.get(nombre="Test Automation")
        self.assertEqual(automatizacion.descripcion, "Descripción de prueba")
        self.assertEqual(automatizacion.version, "1.0")

    def test_ejecucion_creation(self):
        # Prueba de creación de ejecución
        ejecucion = Ejecucion.objects.get(automatizacion=self.automatizacion)
        self.assertEqual(ejecucion.estado, "Completado")

    def test_historial_view(self):
        # Prueba de vista de historial
        response = self.client.get(reverse('historial'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Automation")

    def test_metricas_view(self):
        # Prueba de vista de métricas
        response = self.client.get(reverse('metricas', args=[self.ejecucion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Automation")

    def test_formulario_automatizacion(self):
        # Prueba de formulario de automatización
        response = self.client.post(reverse('crear_automatizacion'), {
            'nombre': 'Nueva Automatización',
            'descripcion': 'Descripción de prueba',
            'version': '1.0',
            'autor': self.usuario.id
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(Automatizacion.objects.filter(nombre='Nueva Automatización').exists())

    def test_formulario_ejecucion(self):
        # Prueba de formulario de ejecución
        response = self.client.post(reverse('crear_ejecucion'), {
            'automatizacion': self.automatizacion.id,
            'timestamp_inicio': '2023-01-01 12:00:00',
            'timestamp_fin': '2023-01-01 13:00:00',
            'estado': 'En progreso'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(Ejecucion.objects.filter(timestamp_inicio='2023-01-01 12:00:00').exists())
