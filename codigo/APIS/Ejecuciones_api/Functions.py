# automation_api.py
import requests
import datetime

API_BASE_URL = "http://localhost:8000/api"
EJECUCIONES_URL = f"{API_BASE_URL}/ejecuciones/"
METRICA_URL = f"{API_BASE_URL}/metrica/"
BITACORA_METRICA_URL = f"{API_BASE_URL}/bitacora-metrica/"

def start_execution(nombre, dispositivo_nombre, automatizacion_nombre):
    data = {
        "nombre": nombre,
        "timestamp_inicio": datetime.datetime.now().isoformat(),
        "estado": "running",
        "dispositivo_nombre": dispositivo_nombre,
        "automatizacion_nombre": automatizacion_nombre
    }
    response = requests.post(EJECUCIONES_URL, json=data)
    if response.status_code == 201:
        execution_id = response.json()['id']
        return execution_id
    elif response.status_code == 400:
        raise Exception("Dispositivo no autorizado")
    elif response.status_code == 404:
        if "Dispositivo" in response.json()["error"]:
            raise Exception("Dispositivo no encontrado")
        else:
            raise Exception("Automatización no encontrada")
    else:
        raise Exception(f"Failed to start execution: {response.text}")

def end_execution(execution_id, estado="completed"):
    data = {
        "estado": estado,
        "timestamp_fin": datetime.datetime.now().isoformat()
    }
    url = f"{EJECUCIONES_URL}{execution_id}/end_execution/"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Execution ended successfully")
    else:
        raise Exception(f"Failed to end execution: {response.text}")

def create_metric_if_not_exists(metrica_nombre):
    response = requests.get(METRICA_URL, params={"nombre": metrica_nombre})
    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    elif response.status_code == 404 or not response.json():
        data = {
            "nombre": metrica_nombre,
            "descripcion": f"Descripción para {metrica_nombre}"
        }
        response = requests.post(METRICA_URL, json=data)
        if response.status_code == 201:
            return response.json()['id']
        else:
            raise Exception(f"Failed to create metric: {response.text}")
    else:
        raise Exception(f"Failed to fetch metric: {response.text}")

def log_metric(ejecucion_id, metrica_nombre, valor):
    metrica_id = create_metric_if_not_exists(metrica_nombre)
    data = {
        "ejecucion": ejecucion_id,
        "metrica_id": metrica_id,
        "valor": valor,
        "FechaRegistro": datetime.datetime.now().date().isoformat(),
        "HoraRegistro": datetime.datetime.now().time().isoformat(),
        "metrica_nombre": metrica_nombre
    }
    response = requests.post(BITACORA_METRICA_URL, json=data)
    if response.status_code == 201:
        print("Metric logged successfully")
    else:
        raise Exception(f"Failed to log metric: {response.text}")
