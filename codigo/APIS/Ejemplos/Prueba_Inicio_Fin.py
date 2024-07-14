from selenium import webdriver
from ejecuciones_api import AutomationAPI

# Configurar la URL base de la API
API_BASE_URL = "http://localhost:8000/api"
automation_api = AutomationAPI(API_BASE_URL)

# Nombre de la automatización
automation_name = "My Selenium Automation"
ejecucion_id = automation_api.start_automation(automation_name)

try:
    driver = webdriver.Chrome()
    driver.get("http://example.com")
    
    # Registrar una variable
    automation_api.log_variable(ejecucion_id, "page_title", driver.title)
    
    # Más código de Selenium aquí...
    
    # Finalizar la automatización
    automation_api.end_automation(ejecucion_id)
except Exception as e:
    # Registrar el fallo de la automatización
    data = {
        "end_time": datetime.datetime.now().isoformat(),
        "status": "failed",
        "error_message": str(e)
    }
    url = f"{automation_api.ejecuciones_url}{ejecucion_id}/"
    requests.patch(url, json=data)
    print(f"Automation failed: {e}")
finally:
    driver.quit()
