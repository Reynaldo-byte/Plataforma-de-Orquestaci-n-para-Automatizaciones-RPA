from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .models import Catalogo, Ejecuciones, BitacoraMetrica, Calendario, Ambientes, Dispositivos,Metrica
from .forms import UsuarioForm, ModificarUsuarioForm, NuevoUsuarioForm, CatalogoForm, EjecucionesForm, BitacoraMetricaForm, CalendarioForm, AmbientesForm, DispositivosForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Catalogo
from .forms import CatalogoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden, HttpResponse
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Count, F, ExpressionWrapper, DurationField
import matplotlib.dates as mdates
import csv

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'mainapp/login.html', {'form': form})

@login_required
def historial_ejecuciones(request):
    ejecuciones = Ejecuciones.objects.all()
    return render(request, 'mainapp/historial_ejecuciones.html', {'ejecuciones': ejecuciones})
def metricas(request, ejecucion_id):
    metricas = BitacoraMetrica.objects.filter(ejecucion_id=ejecucion_id)
    detalles_metricas = []

    for metrica in metricas:
        metrica_nombre = Metrica.objects.get(id=metrica.metrica_id).nombre
        detalles_metricas.append({
            'metrica': metrica,
            'nombre': metrica_nombre
        })

    return render(request, 'mainapp/metricas.html', {'ejecucion_id': ejecucion_id, 'detalles_metricas': detalles_metricas})
@login_required
def detalle_automatizacion(request, automatizacion_id):
    automatizacion = get_object_or_404(Catalogo, pk=automatizacion_id)
    return render(request, 'mainapp/detalle_automatizacion.html', {'automatizacion': automatizacion})

@login_required
def modificar_automatizacion(request, automatizacion_id):
    automatizacion = get_object_or_404(Catalogo, pk=automatizacion_id)
    if request.method == "POST":
        form = CatalogoForm(request.POST, instance=automatizacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_automatizacion', automatizacion_id=automatizacion.id)
    else:
        form = CatalogoForm(instance=automatizacion)
    return render(request, 'mainapp/modificar_automatizacion.html', {'form': form})

@login_required
def calendario_ejecucion(request):
    calendarios = Calendario.objects.all()
    return render(request, 'mainapp/calendario_ejecucion.html', {'calendarios': calendarios})

@login_required
def nueva_ejecucion(request):
    if request.method == "POST":
        form = EjecucionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendario_ejecucion')
    else:
        form = EjecucionesForm()
    return render(request, 'mainapp/nueva_ejecucion.html', {'form': form})

@login_required
def detalle_ejecucion(request, calendario_id):
    calendario = get_object_or_404(Calendario, pk=calendario_id)
    return render(request, 'mainapp/detalle_ejecucion.html', {'calendario': calendario})

@login_required
def modificar_ejecucion(request, calendario_id):
    calendario = get_object_or_404(Calendario, pk=calendario_id)
    if request.method == "POST":
        form = CalendarioForm(request.POST, instance=calendario)
        if form.is_valid():
            form.save()
            return redirect('detalle_ejecucion', calendario_id=calendario.id)
    else:
        form = CalendarioForm(instance=calendario)
    return render(request, 'mainapp/modificar_ejecucion.html', {'form': form})

@login_required
def ambientes(request):
    ambientes = Ambientes.objects.all()
    return render(request, 'mainapp/ambientes.html', {'ambientes': ambientes})

@login_required
def nuevo_ambiente(request):
    if request.method == "POST":
        form = AmbientesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ambientes')
    else:
        form = AmbientesForm()
    return render(request, 'mainapp/nuevo_ambiente.html', {'form': form})

@login_required
def detalle_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(Ambientes, pk=ambiente_id)
    return render(request, 'mainapp/detalle_ambiente.html', {'ambiente': ambiente})

@login_required
def modificar_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(Ambientes, pk=ambiente_id)
    if request.method == "POST":
        form = AmbientesForm(request.POST, instance=ambiente)
        if form.is_valid():
            form.save()
            return redirect('detalle_ambiente', ambiente_id=ambiente.id)
    else:
        form = AmbientesForm(instance=ambiente)
    return render(request, 'mainapp/modificar_ambiente.html', {'form': form})

@login_required
def dispositivos(request):
    dispositivos = Dispositivos.objects.all()
    return render(request, 'mainapp/dispositivos.html', {'dispositivos': dispositivos})

@login_required
def nuevo_dispositivo(request):
    if request.method == "POST":
        form = DispositivosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos')
    else:
        form = DispositivosForm()
    return render(request, 'mainapp/nuevo_dispositivo.html', {'form': form})

@login_required
def detalle_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivos, pk=dispositivo_id)
    return render(request, 'mainapp/detalle_dispositivo.html', {'dispositivo': dispositivo})

@login_required
def modificar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivos, pk=dispositivo_id)
    if request.method == "POST":
        form = DispositivosForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('detalle_dispositivo', dispositivo_id=dispositivo.id)
    else:
        form = DispositivosForm(instance=dispositivo)
    return render(request, 'mainapp/modificar_dispositivo.html', {'form': form})


@login_required

def usuarios(request):
    usuarios = User.objects.exclude(pk=request.user.pk)
    return render(request, 'mainapp/usuarios.html', {'usuarios': usuarios})


@login_required
def detalle_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    return render(request, 'mainapp/detalle_usuario.html', {'usuario': usuario})

@login_required

def nuevo_usuario(request):
    if not request.user.has_perm('auth.add_user'):
        return render(request, 'mainapp/permisos_insuficientes.html')
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'mainapp/nuevo_usuario.html', {'form': form})


@login_required
def modificar_usuario(request, usuario_id):
    if not request.user.has_perm('auth.change_user'):
        return render(request, 'mainapp/permisos_insuficientes.html')
    usuario = get_object_or_404(User, pk=usuario_id)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('detalle_usuario', usuario_id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'mainapp/modificar_usuario.html', {'form': form})

def eliminar_usuario(request, usuario_id):
    

    # Verificar si el usuario tiene permiso para eliminar usuarios
    if not request.user.has_perm('auth.delete_user'):
        return render(request, 'mainapp/permisos_insuficientes.html')
    usuario = get_object_or_404(User, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios')

    return render(request, 'mainapp/eliminar_usuario.html', {'objeto': usuario})
@login_required
# Vista para eliminar ejecución
def eliminar_ejecucion(request, calendario_id):
    calendario = get_object_or_404(Calendario, pk=calendario_id)
    if request.method == 'POST':
        calendario.delete()
        return redirect('calendario_ejecucion')
    return render(request, 'mainapp/eliminar_confirmacion.html', {'objeto': calendario})

@login_required
# Vista para eliminar ambiente
def eliminar_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(Ambientes, pk=ambiente_id)
    if request.method == 'POST':
        ambiente.delete()
        return redirect('ambientes')
    return render(request, 'mainapp/eliminar_confirmacion.html', {'objeto': ambiente})

@login_required
# Vista para eliminar dispositivo
def eliminar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivos, pk=dispositivo_id)
    if request.method == 'POST':
        dispositivo.delete()
        return redirect('dispositivos')
    return render(request, 'mainapp/eliminar_confirmacion.html', {'objeto': dispositivo})

# mainapp/views.py

@login_required
def home(request):
    return render(request, 'mainapp/home.html')


@login_required
def catalogo(request):
    catalogos = Catalogo.objects.all()
    return render(request, 'mainapp/catalogo.html', {'catalogos': catalogos})

@login_required
def crear_automatizacion(request):
    if request.method == "POST":
        form = CatalogoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = CatalogoForm()
    return render(request, 'mainapp/crear_automatizacion.html', {'form': form})

@login_required
def modificar_automatizacion(request, automatizacion_id):
    automatizacion = get_object_or_404(Catalogo, pk=automatizacion_id)
    if request.method == "POST":
        form = CatalogoForm(request.POST, instance=automatizacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_automatizacion', automatizacion_id=automatizacion.id)
    else:
        form = CatalogoForm(instance=automatizacion)
    return render(request, 'mainapp/modificar_automatizacion.html', {'form': form})

@login_required
def detalle_automatizacion(request, automatizacion_id):
    automatizacion = get_object_or_404(Catalogo, pk=automatizacion_id)
    return render(request, 'mainapp/detalle_automatizacion.html', {'automatizacion': automatizacion})

@login_required
def eliminar_automatizacion(request, automatizacion_id):
    automatizacion = get_object_or_404(Catalogo, pk=automatizacion_id)
    if request.method == 'POST':
        automatizacion.delete()
        return redirect('catalogo')
    return render(request, 'mainapp/eliminar_automatizacion.html', {'objeto': automatizacion})
@login_required
def verificar_permisos(request):
    permisos = {
        'auth.view_user': request.user.has_perm('auth.view_user'),
        'auth.add_user': request.user.has_perm('auth.add_user'),
        'auth.change_user': request.user.has_perm('auth.change_user'),
        'auth.delete_user': request.user.has_perm('auth.delete_user'),
    }
    return HttpResponse(f'Permisos del usuario: {permisos}')

@login_required
def dashboard(request):
    # Obtener parámetros seleccionados por el usuario
    dispositivo_id = request.GET.get('dispositivo')
    automatizacion_id = request.GET.get('automatizacion')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar ejecuciones por dispositivo, automatización y rango de fechas si se seleccionaron
    filtros = {}
    dispositivo_nombre = "Todos los dispositivos"
    automatizacion_nombre = "Todas las automatizaciones"
    
    if dispositivo_id:
        filtros['dispositivo_id'] = dispositivo_id
        dispositivo_nombre = Dispositivos.objects.get(id=dispositivo_id).nombre
    if automatizacion_id:
        filtros['automatizacion_id'] = automatizacion_id
        automatizacion_nombre = Catalogo.objects.get(id=automatizacion_id).nombre
    if fecha_inicio:
        filtros['timestamp_inicio__gte'] = fecha_inicio
    if fecha_fin:
        filtros['timestamp_inicio__lte'] = fecha_fin

    # Número de ejecuciones por dispositivo
    ejecuciones_por_dispositivo = Ejecuciones.objects.filter(**filtros).values('dispositivo__nombre').annotate(total=Count('id'))

    # Contar el número de ejecuciones por día
    ejecuciones_por_dia = Ejecuciones.objects.filter(**filtros).values('timestamp_inicio__date').annotate(total=Count('id'))

    fechas = [ejecucion['timestamp_inicio__date'] for ejecucion in ejecuciones_por_dia]
    cantidades = [ejecucion['total'] for ejecucion in ejecuciones_por_dia]

    # Crear gráfico de línea: Número de Ejecuciones por Día
    fig, ax = plt.subplots(figsize=(12, 6))
    if fechas and cantidades:
        ax.plot(fechas, cantidades, marker='o', linestyle='-', color='b')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Número de Ejecuciones')
        ax.set_title(f'Número de Ejecuciones por Día ({automatizacion_nombre})')

       
        if fecha_inicio and fecha_fin:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            if fecha_inicio_dt == fecha_fin_dt:
                fecha_fin_dt += timedelta(days=1)
            ax.set_xlim([fecha_inicio_dt, fecha_fin_dt])

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  
        fig.autofmt_xdate()

        plt.xticks(rotation=45)
    else:
        ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Número de Ejecuciones')
        ax.set_title(f'Número de Ejecuciones por Día ({automatizacion_nombre})')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    grafico_linea = base64.b64encode(image_png).decode('utf-8')

   
    estados_conteo = Ejecuciones.objects.filter(**filtros).values('estado').annotate(total=Count('id'))
    estados = [estado['estado'] for estado in estados_conteo]
    conteos = [estado['total'] for estado in estados_conteo]
    total_ejecuciones = sum(conteos)

    fig, ax = plt.subplots(figsize=(8, 8))
    if conteos:
        wedges, texts, autotexts = ax.pie(conteos, labels=estados, autopct='%1.1f%%', startangle=90, textprops=dict(color="w"))
        plt.setp(autotexts, size=10, weight="bold")
        ax.set_title(f"Estados de Ejecuciones (Total: {total_ejecuciones})")
    else:
        ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(f"Estados de Ejecuciones (Total: 0)")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    grafico_circular = base64.b64encode(image_png).decode('utf-8')

  
    dispositivos = [d['dispositivo__nombre'] for d in ejecuciones_por_dispositivo]
    totales = [d['total'] for d in ejecuciones_por_dispositivo]

    fig, ax = plt.subplots(figsize=(12, 6))
    if dispositivos and totales:
        ax.bar(dispositivos, totales)
        ax.set_xlabel('Dispositivos')
        ax.set_ylabel('Número de Ejecuciones')
        ax.set_title(f'Número de Ejecuciones por Dispositivo ({dispositivo_nombre})')
    else:
        ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_xlabel('Dispositivos')
        ax.set_ylabel('Número de Ejecuciones')
        ax.set_title(f'Número de Ejecuciones por Dispositivo ({dispositivo_nombre})')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    grafico_barras = base64.b64encode(image_png).decode('utf-8')


    dispositivos = Dispositivos.objects.all()
    automatizaciones = Catalogo.objects.all()

    context = {
        'grafico_barras': grafico_barras,
        'grafico_linea': grafico_linea,
        'grafico_circular': grafico_circular,
        'dispositivos': dispositivos,
        'automatizaciones': automatizaciones,
        'selected_dispositivo': dispositivo_id,
        'selected_automatizacion': automatizacion_id,
        'selected_fecha_inicio': fecha_inicio,
        'selected_fecha_fin': fecha_fin
    }

    return render(request, 'mainapp/dashboard.html', context)


def exportar_metricas(request, ejecucion_id):
    ejecucion = Ejecuciones.objects.get(id=ejecucion_id)
    automatizacion = Catalogo.objects.get(id=ejecucion.automatizacion_id)
    metricas = BitacoraMetrica.objects.filter(ejecucion_id=ejecucion_id)
    detalles_metricas = []

    for metrica in metricas:
        metrica_nombre = Metrica.objects.get(id=metrica.metrica_id).nombre
        detalles_metricas.append({
            'metrica': metrica,
            'nombre': metrica_nombre
        })

    
    nombre_automatizacion = automatizacion.nombre.replace(' ', '_')
    fecha_ejecucion = ejecucion.timestamp_inicio.strftime('%Y-%m-%d')
    nombre_archivo = f'metricas_{nombre_automatizacion}_{fecha_ejecucion}.csv'


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    writer = csv.writer(response)
    writer.writerow(['ID de Ejecución', 'Nombre de la Métrica', 'Valor', 'Fecha de Registro', 'Hora de Registro'])

    for detalle in detalles_metricas:
        metrica = detalle['metrica']
        fecha_registro = metrica.FechaRegistro.strftime('%Y-%m-%d') if metrica.FechaRegistro else ''
        hora_registro = metrica.HoraRegistro.strftime('%H:%M:%S') if metrica.HoraRegistro else ''
        writer.writerow([metrica.ejecucion_id, detalle['nombre'], metrica.valor, fecha_registro, hora_registro])

    return response