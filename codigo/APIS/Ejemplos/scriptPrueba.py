# script_selenium.py
from selenium import webdriver
from Functions import start_execution, end_execution, log_metric

# Inicializar el driver de Selenium
driver = webdriver.Chrome()

# Empezar la automatización
execution_id = start_execution("Prueba de Automatización", dispositivo_nombre="Dispositivo1", automatizacion_id=1)

try:
    # Tu código de Selenium aquí
    driver.get("http://example.com")
    # Log metrics
    log_metric(execution_id, metrica_id=1, valor=123.45)

    # Finalizar la automatización exitosamente
    end_execution(execution_id)
except Exception as e:
    # Registrar el fallo de la automatización
    end_execution(execution_id, estado="failed")
    print(f"Automation failed: {e}")
finally:
    # Cerrar el driver de Selenium
    driver.quit()
