from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

def localizar_elemento(navegador, xpath):
    while True:
        try:
            elemento = navegador.find_element(By.XPATH, xpath)
            return elemento
        except StaleElementReferenceException:
            continue
