import sys
import requests
import json
from bs4 import BeautifulSoup
import re
import textwrap

# Función para convertir el tiempo "min:seg" en segundos
def convertir_a_segundos(tiempo):
    minutos, segundos = map(int, tiempo.split(":"))
    return minutos * 60 + segundos

# Función para reemplazar tiempos "min:seg" por segundos
def reemplazar_tiempo(match):
    peso = match.group(1)
    tiempo = match.group(2)
    segundos = convertir_a_segundos(tiempo)
    return f"{peso} x {segundos} sec"

def procesar_url(url):
    print(f'Procesando URL: {url}')

    # Convertir la URL a formato de API
    api_url = re.sub(r'/notice/', r'//api/v1/statuses/', url)

    # Solicitar la URL
    response = requests.get(api_url)

    # Comprobar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al solicitar la URL: {response.status_code}")
        sys.exit(1)

    # Eliminar los tags <br> convirtiéndolos en saltos de línea
    contenido = re.sub(r'<br/>', '\n', response.json()['content'])

    # Convertir el contenido HTML a texto plano
    soup = BeautifulSoup(contenido, 'html.parser')
    texto_plano = soup.text

    # Formateo del contenido para WeightXReps
    texto_formateado = re.sub(r'#', '', texto_plano)
    texto_formateado = re.sub(r'[1-9]\. ', '', texto_formateado)
    texto_formateado = re.sub(r' Reps', '', texto_formateado)
    texto_formateado = re.sub(r'Kg ', '', texto_formateado)
    texto_formateado = textwrap.indent(texto_formateado, '#')

    # Reemplazo de tiempos y ajustes
    texto_formateado = re.sub(r"(\d+)\s*Kg\s*x\s*(\d+:\d+)", reemplazar_tiempo, texto_formateado)
    texto_formateado = re.sub(r'#Punching', 'Cardio: Punching', texto_formateado)
    # En caso de que hayan ejercicios de calistenia, añadir BW (Bodyweight)
    texto_formateado = re.sub(r'# x', 'BW x', texto_formateado)
    
    #eliminar # al comienzo de la línea cuando lo que sigue son ejercicios
    texto_formateado = re.sub(r'^#(\d)', r'\1', texto_formateado, flags=re.MULTILINE)

    return texto_formateado

def guardar_en_archivo(contenido, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        archivo.writelines(contenido)
    print(f"Archivo guardado como {nombre_archivo}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python plrm2wxr.py URL")
        sys.exit(1)

    url = re.sub(r"'\]", '', re.sub(r"\['", '', str(sys.argv[1:])))
    contenido_procesado = procesar_url(url)
    
    # Imprimir el contenido procesado en consola
    print(contenido_procesado)
    
    # Guardar el contenido en un archivo de texto
    guardar_en_archivo(contenido_procesado, 'plrm2wxr.txt')
