
import random
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent



from options import options_list

options = webdriver.ChromeOptions()

for option in options_list:
    options.add_argument(option)

user_agent = UserAgent()

options.add_argument(f'--user-agent={user_agent.random}')
time.sleep(2)

driver = webdriver.Chrome(options=options)

with open('walmart_department\proxfile.txt', 'r') as f:
    lineas = f.readlines()
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

print('----------Initializing Scraper----------')

url_web = 'https://super.walmart.com.mx/'
driver.get(url_web)

time.sleep(2)

time.sleep(random.uniform(3, 6))

wait = WebDriverWait(driver, 5)

xpath_page_root = '//*[@id="__next"]'
xpath_department = '//*[@id="__next"]/div[1]/div/span/header/section[1]/div/button'
xpath_categories_section = '//*[@id="__next"]/div[1]/div/span/header/section/div/div/div/div/div/ul/li[4]/button'
xpath_category_columns = '//*[@id="__next"]/div[1]/div/span/header/section/div/div/div/div/section/div/ul'
xpath_child_div_abarrotes = '//*[@id="__next"]/div[1]/div/span/header/section/div/div/div/div/section/div/ul/div[1]'

time.sleep(2)

while True:
    print('----------NO HUMAN DETECTED --------')
    print('-----attempting to skip captcha ---------')
    time.sleep(2)
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
        for i in range(2):
            if(i == 1):
                driver.get(url_web)
                PROXY = random.choice(lineas)
                webdriver.DesiredCapabilities.CHROME['proxy']={
                    "httpProxy":PROXY,
                    "ftpProxy":PROXY,
                    "sslProxy":PROXY,
                    "noProxy":None,
                    "proxyType":"MANUAL",
                    "class":"org.openqa.selenium.Proxy",
                    "autodetect":False
                }
                print('Asignando nueva direccion: ' + PROXY)
                print('---En caso de superar los 5 intentos, intentar con una lista de proxy diferente/nueva--- o reiniciar el scraper despues de 5 minutos desde su ultima ejecucion')
                i = 0
            else:
                i=i + 1
    except NoSuchElementException:
        break
    except StaleElementReferenceException:
        continue



print('-----index page -----')
btn_categories = driver.find_element(By.XPATH, xpath_department)
time.sleep(2)
btn_categories.click()
print('---Click btn_categories---')

wait.until(EC.visibility_of_element_located((By.XPATH, xpath_categories_section)))

abarrotes_seccion = driver.find_element(By.XPATH, xpath_categories_section)
time.sleep(2)
abarrotes_seccion.click()
print('---Click abarrotes_seccion---')


get_category_columns = driver.find_element(By.XPATH, xpath_category_columns)
time.sleep(2)
child_div_elements = get_category_columns.find_elements(By.XPATH, './div')

jsonobjet = {
    "department": "Abarrotes",
    "url": "https://super.walmart.com.mx/content/abarrotes/120005",
    "categories": [
    ],
}
print('---creando JSON---')
time.sleep(2)
for element in child_div_elements:
    ('---Comenzando iteracion---')
    li_element = element.find_elements(By.XPATH, './li')

    for child_e in li_element:

        category_obj = {}
        subcategories_array = []
        h2_element = child_e.find_elements(By.XPATH, './h2')
        category = h2_element[0].text
        category_obj['category'] = category
        ul_element = child_e.find_elements(By.XPATH, './ul')

        for e in ul_element:

            li_items = e.find_elements(By.XPATH, './li')
            for li in li_items:
                if(li.text == 'Ver todo'):
                    a_element = li.find_elements(By.XPATH, './a')
                    href = a_element[0].get_attribute('href')
                    category_obj['url'] = href

                else:
                    a_element = li.find_elements(By.XPATH, './a')
                    href = a_element[0].get_attribute('href')
                    subcategory_name = a_element[0].text

                    subcat_obj = {"subcategory": subcategory_name, "url": href}
                    subcategories_array.append(subcat_obj)

        category_obj['subcategories'] = subcategories_array
        jsonobjet['categories'].append(category_obj)
print('---Generando fichero JSON---')
json_clean = json.dumps(jsonobjet, ensure_ascii=False)    

print('------------SCRAPPER FINALIZADO------------')
print(json_clean)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(json_clean, f, ensure_ascii=False, indent=4)

driver.quit()