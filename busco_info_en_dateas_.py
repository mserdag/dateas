#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd
import random


# Leo el data set que me va a permitir buscar los datos en la pagina web

df_dni = pd.read_csv(r'Aca va el archivo CSV')

if 'edad' in df_dni.columns:
    posiciones = df_dni[df_dni['edad'] == 999].index    
    
if len(posiciones) == 0:
    posiciones = 0
else:
    posiciones = df_dni[df_dni['edad'] == 999].index[0]
    
print(posiciones)

# llamo a la pagina web
def inicio_pag_web():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # Modo incógnito
    options.add_argument("--start-maximized") # Pagina Maximizada 
    options.add_argument("--headless")  # Ejecutar Chrome en modo headless (sin interfaz gráfica)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.dateas.com/es/consulta_cuit_cuil")
    return driver

def extraigo_info(dni):
    #busco el box de cuit-cuil-dni
    cuit = driver.find_element(By.ID, "cuit-cuil-dni")

    #cuando lo encuentro doy click
    driver.find_element(By.ID, "cuit-cuil-dni").click()

    #escribo dentro, "Displayed", es un ejemplo
    cuit.send_keys(dni)
    cuit.send_keys(Keys.RETURN)   
    
    try: # Me fijo si esa persona existe
        # luego de presionar paso al siguiente nivel
        boton = driver.find_element(By.XPATH, '//*[@id="main-content"]/table/tbody/tr/td[3]/a')
        boton.send_keys(Keys.RETURN)
        # Edad estimada
        dato = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/table/tbody/tr[4]/td')
        edad = dato.text        
    except NoSuchElementException:
        # no existe en la base de datos
        
        #respuesta = driver.find_element(By.XPATH, '//*[@id="main-content"]/h2')
        # Cuando el dni no existe se le asigna 0 años
        edad = '0 años'
        
        # Eliminar todas las cookies
    
    driver.delete_all_cookies()
    return (edad)


# Recorro el data set y busco en la pagina web buscando los datos

edad_participante = []

# es para que en caso que se haya suspendido la carga inicie desde donde la 
# dejo y no desde el principio

inicio = posiciones 
if inicio > 0:
    edad_participante = df_dni['edad'][df_dni['edad'] != 999].tolist()
    #edad_participante = df_dni['edad'].tolist()

while inicio < len(df_dni):    
    for j in range(inicio, len(df_dni)):
        driver = inicio_pag_web()
        time.sleep(random.uniform(1, 5))  # Pausa de entre 1 y 5 segundos
        if len(df_dni)-inicio > 8:
            cantidad = 8
        else:
            cantidad = len(df_dni)-inicio
        for h in range (cantidad):
            dni = df_dni['DNI'][inicio+h]
            dni = int(dni)
            edad = extraigo_info(dni)
            try:
                edad = int(edad.split()[0])
            except:
                edad = 0
            edad_participante.append(edad) 
            print(inicio+h, dni, edad_participante[inicio+h])
            time.sleep(random.uniform(1, 15))  # Pausa de entre 1 y 5 segundos
                
        inicio = len(edad_participante)
        print('Salto')
        driver.quit()
        df_dni['edad'] = edad_participante + [999] * (len(df_dni) - len(edad_participante))
        df_dni.to_csv(r'aca guardo el archivo de destino', index=False)
        time.sleep(random.uniform(1, 120))  # Pausa de entre 1 y 5 segundos

# Salgo de la pagina y cierro el navegador

driver.quit()
print('Termine')


