# mainapp/forms.py

from django import forms
from .models import Catalogo, Ejecuciones, BitacoraMetrica, Calendario, Ambientes, Dispositivos
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User, Group
from .models import Dispositivos, SistemaOperativo, SsdCapacidad, Memoria, Resolucion
class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = ['nombre', 'descripcion', 'version', 'autor']
        widgets = {
            'autor': forms.Select(),
        }

from django import forms
from .models import Ejecuciones, Dispositivos

class EjecucionesForm(forms.ModelForm):
    dispositivo = forms.ModelChoiceField(queryset=Dispositivos.objects.all(), required=True)

    class Meta:
        model = Ejecuciones
        fields = ['nombre', 'timestamp_inicio', 'estado', 'dispositivo', 'automatizacion']
        widgets = {
            'timestamp_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
            'estado': forms.Select(choices=[('Pendiente', 'Pendiente'), ('En Progreso', 'En Progreso'), ('Finalizado', 'Finalizado')]),
        }


class BitacoraMetricaForm(forms.ModelForm):
    class Meta:
        model = BitacoraMetrica
        fields = ['ejecucion', 'metrica_id', 'valor', 'FechaRegistro', 'HoraRegistro']
        widgets = {
            'FechaRegistro': forms.DateInput(attrs={'type': 'date'}),
            'HoraRegistro': forms.TimeInput(attrs={'type': 'time'}),
        }

class CalendarioForm(forms.ModelForm):
    class Meta:
        model = Calendario
        fields = ['automatizacion', 'fecha_programada', 'hora_programada']
        widgets = {
            'fecha_programada': forms.DateInput(attrs={'type': 'date'}),
            'hora_programada': forms.TimeInput(attrs={'type': 'time'}),
        }

class AmbientesForm(forms.ModelForm):
    class Meta:
        model = Ambientes
        fields = ['nombre_ambiente', 'descripcion']

class DispositivosForm(forms.ModelForm):
    so = forms.ModelChoiceField(queryset=SistemaOperativo.objects.all())
    ssd = forms.ModelChoiceField(queryset=SsdCapacidad.objects.all())
    memoria_ram = forms.ModelChoiceField(queryset=Memoria.objects.all())
    resolucion = forms.ModelChoiceField(queryset=Resolucion.objects.all())

    class Meta:
        model = Dispositivos
        fields = ['nombre', 'estado', 'memoria_ram', 'ssd', 'resolucion', 'so']
        widgets = {
            'estado': forms.Select(choices=[('Disponible', 'Disponible'), ('No Disponible', 'No Disponible')]),
        }
class UsuarioForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'roles']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['roles'])
        return user

class ModificarUsuarioForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'roles']
        

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['roles'])
        return user

class NuevoUsuarioForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'roles']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['roles'])
        return user
