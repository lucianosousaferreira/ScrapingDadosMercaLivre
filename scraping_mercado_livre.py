from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import time as t
import pandas as pd
from bs4 import BeautifulSoup

options=Options()
#options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9515')
options.add_argument('--disable-setuid-sandbox')

driver = webdriver.Firefox()
list_aplic = []

driver.get('https://www.mercadolivre.com.br/')
t.sleep(2)
driver.get('https://lista.mercadolivre.com.br/junta-cabe%C3%A7ote#D[A:JUNTA%20CABE%C3%87OTE]')
t.sleep(3)

#seleciona marca
driver.find_element(By.NAME,'BRAND').click()
t.sleep(1)
list_marc = driver.find_elements(By.CLASS_NAME,'andes-list__item-first-column')

for i in tqdm(range(0,len(list_marc))):

    brand = driver.find_elements(By.CLASS_NAME,'andes-list__item-first-column')[i]
    while brand.is_displayed() == False:
        t.sleep(0.7)
    driver.execute_script("arguments[0].click();",brand)
    driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[2]/section/div[1]').click()
    t.sleep(0.5)
    html_mc = driver.execute_script("return document.documentElement.outerHTML")
    t.sleep(0.5)
    soup = BeautifulSoup(html_mc,"html.parser")
    marca = soup.find_all('span',class_='andes-dropdown__display-values')[1]
    t.sleep(0.5)


    #selecionando modelo
    driver.find_element(By.NAME,'MODEL').click()
    for model in driver.find_elements(By.CLASS_NAME,'andes-list__item-first-column'):
        try:
            while model.is_displayed() == False:
                t.sleep(0.7)
            driver.execute_script("arguments[0].click();",model)
            driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[2]/section/div[1]').click()
            t.sleep(0.5)
            html_vc = driver.execute_script("return document.documentElement.outerHTML")
            t.sleep(0.5)
            soup2 = BeautifulSoup(html_vc,"html.parser")
            modelo = soup2.find_all('span',class_='andes-dropdown__display-values')[2]
            t.sleep(0.5)

        except IndexError:
            pass


        #selecionando ano
        driver.find_element(By.NAME,'VEHICLE_YEAR').click()

        for year in driver.find_elements(By.CLASS_NAME,'andes-list__item-first-column'):
            try:
                while year.is_displayed() == False:
                    t.sleep(0.7)
                driver.execute_script("arguments[0].click();",year)
                driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[2]/section/div[1]').click()
                t.sleep(0.5)
                html_year = driver.execute_script("return document.documentElement.outerHTML")
                t.sleep(0.5)
                soup3 = BeautifulSoup(html_year,"html.parser")
                ano = soup3.find_all('span',class_='andes-dropdown__display-values')[3]
                t.sleep(0.5)

            except IndexError:
                pass

            #selecionando versão

            driver.find_element(By.NAME,'TRIM').click()
            for trim in driver.find_elements(By.CLASS_NAME,'andes-list__item-first-column'):
                try:
                    while trim.is_displayed() == False:
                        t.sleep(0.7)
                    driver.execute_script("arguments[0].click();",trim)
                    driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[2]/section/div[1]').click()
                    t.sleep(0.5)
                    html_vs = driver.execute_script("return document.documentElement.outerHTML")
                    t.sleep(0.5)
                    soup4 = BeautifulSoup(html_vs,"html.parser")
                    vers = soup4.find_all('span',class_='andes-dropdown__display-values')[4]
                    t.sleep(0.5)
                    list_aplic.append(marca.text +';'+ modelo.text +';'+ ano.text +';'+ vers.text)
                    #print(marca.text +';'+ modelo.text +';'+ ano.text +';'+ vers.text)
                except IndexError:
                    pass
                driver.find_element(By.NAME,'TRIM').click()
                t.sleep(0.7)
            driver.find_element(By.NAME,'VEHICLE_YEAR').click()
            t.sleep(0.7)
        driver.find_element(By.NAME,'MODEL').click()
        t.sleep(0.7)
    driver.find_element(By.NAME,'BRAND').click()
    t.sleep(0.7)

df = pd.DataFrame([list_aplic]).T
df = df[0].str.split(';',expand=True)
df.rename(columns={0:'BRAND',1:'MODEL',2:'VEHICLE_YEAR',3:'TRIM'},inplace=True)
df.to_excel('aplicações_Mercado_Livre.xlsx',index=False)
    

driver.close()
driver.quit()
