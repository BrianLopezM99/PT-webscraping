import random
import sys
import time
import os
import json
import random

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent

from dotenv import load_dotenv

from options import options_list

options = webdriver.ChromeOptions()

for option in options_list:
    options.add_argument(option)

# Configuración del proxy

# Abrir el archivo y obtener todas las líneas como una lista
with open('./proxfile.txt', 'r') as f:
    lineas = f.readlines()

# Obtener una fila aleatoria de la lista de líneas
PROXY = random.choice(lineas)

# Imprimir la fila aleatoria
print(PROXY)
 # IP:PUERTO del proxy
webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

ua = UserAgent(browsers=['chrome'])
user_agent = ua.random

options.add_argument(f'--user-agent={user_agent}')

driver = webdriver.Chrome(options=options)

load_dotenv()

url_web = os.getenv("URL_SITE_INDEX")
driver.implicitly_wait(10)
driver.get('https://super.walmart.com.mx/browse/abarrotes/abarrotes-de-nuestras-marcas/despensa-basica/120005_4130241_4130242')

time.sleep(random.uniform(1, 4))

wait = WebDriverWait(driver, 5)
data = {
    "url": "https://super.walmart.com.mx/browse/abarrotes/abarrotes-de-nuestras-marcas/despensa-basica/120005_4130241_4130242",
    "products": []
}


while True:
    try:
        xpath_captcha = '//*[@id="px-captcha"]'
        human = driver.find_element(By.XPATH, xpath_captcha)
        action = ActionChains(driver)
        click = ActionChains(driver)
        action.click_and_hold(human)
        action.perform()
        time.sleep(10)
        action.release(human)
        action.perform()
        time.sleep(0.2)
        action.release(human)
    except NoSuchElementException:
        break
    except StaleElementReferenceException:
        continue

xpath_products_container = '//*[@id="maincontent"]/main/div/div/div/div/div[3]/div[2]/div/section/div/div'

xpath_products_container2 = '//*[@id="maincontent"]/main/div/div/div/div/div[3]/div/div/section/div/div'

xpath_navigation_container = '//*[@id="maincontent"]/main/div/div/div/div/div[4]/nav/ul/li'

list_items = driver.find_elements(By.XPATH, xpath_products_container)



elements_navigator = driver.find_elements(By.XPATH, xpath_navigation_container)

for i in elements_navigator:
    
    while True:
        try:
            xpath_captcha = '//*[@id="px-captcha"]'
            human = driver.find_element(By.XPATH, xpath_captcha)
            action = ActionChains(driver)
            click = ActionChains(driver)
            action.click_and_hold(human)
            action.perform()
            time.sleep(10)
            action.release(human)
            action.perform()
            time.sleep(0.2)
            action.release(human)
        except NoSuchElementException:
            break
        except StaleElementReferenceException:
            continue
    
    elements_navigator = driver.find_elements(By.XPATH, xpath_navigation_container)
    element_found = False

    for count, element in enumerate(elements_navigator):
        if count == 0:
            continue
        try:
            i_tag = element.find_elements(By.XPATH, './a/i')
            if(len(i_tag) > 0):

                element_found = True
                break
            else:
                continue
        except NoSuchElementException:
            continue
    list_items = driver.find_elements(By.XPATH, xpath_products_container)
    list_items2 = driver.find_elements(By.XPATH, xpath_products_container)
    if element_found:
        # Realizar acciones si se encuentra el elemento
        for item in list_items:
            obj = item.text
            obj_arr = obj.split("\n")
            new_product = {
                "name": obj_arr[0],
                "current_price": obj_arr[3] if len(obj_arr) > 6 else obj_arr[2],
                "original_price": obj_arr[5] if len(obj_arr) > 6 else obj_arr[2]
            }
            time.sleep(1)
            data["products"].append(new_product)
            time.sleep(1)
             
        time.sleep(8)
        i_tag[0].click()
        i_tag.clear()
    else:
        # Realizar acciones si no se encuentra el elemento
        for item in list_items:
            obj = item.text
            obj_arr = obj.split("\n")
            new_product = {
                "name": obj_arr[0],
                "current_price": obj_arr[3] if len(obj_arr) > 6 else obj_arr[2],
                "original_price": obj_arr[5] if len(obj_arr) > 6 else obj_arr[2]
            }
            data["products"].append(new_product)

        print('Elemento no encontrado, se ha finalizado la paginacion')

json_data = json.dumps(data)

print(json_data)
    

# # Recupere el parámetro pasado por Node.js
# parametro = sys.argv[1]

# # Use el parámetro en su script de Python
# resultado = parametro

# Imprima el resultado para que Node.js pueda leerlo
print('resultado de walmart_products: ' + json_data + 'De la URL: TEST')
