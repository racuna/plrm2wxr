import sys
import requests
import json
from bs4 import BeautifulSoup
import re
import textwrap

# Función para convertir el tiempo "min:seg" en segundos
def convertir_a_segundos(tiempo):
    """
    Args:
    el tiempo de un ejercicio en formato MM:SS

    Returns:
    Retorna en una cifra en segundos
    """
    minutos, segundos = map(int, tiempo.split(":"))
    return minutos * 60 + segundos

# Función para reemplazar ejercicios basados en tiempo a segundos
def reemplazar_tiempo(match):
    peso = match.group(1)
    tiempo = match.group(2)
    segundos = convertir_a_segundos(tiempo)
    return f"{peso} x {segundos} sec"

def procesar_url(url):
    """
    Args:
    recibe una URL de un post de pleroma

    Returns:
    Retorna el contenido del post en texto, además en un formato que entienda WeightXReps
    """
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
    
def encontrar_primera_serie(contenido_procesado):
  """Encuentra el índice de la primera línea que inicia con un número.

  Args:
    contenido_procesado: El contenido procesado del sitio web, en formato de lista de líneas.

  Returns:
    El índice de la primera línea que inicia con un número, o None si no se encuentra.
  """

  for i, linea in enumerate(contenido_procesado):
    if linea and linea[0].isdigit():
      return i + 1  # Sumamos 1 para obtener el índice en base 1
  return None

def eliminar_hashes_hasta_linea(contenido_procesado, primer_serie):
  """Elimina los símbolos # al inicio de las líneas hasta la línea primer_serie-2.

  Args:
    contenido_procesado: El contenido procesado del sitio web, en formato de lista de líneas.
    primer_serie: El índice de la primera línea que inicia con un número.

  Returns:
    Una nueva lista de líneas con los hashes eliminados hasta la línea indicada.
  """

  resultado = []
  for i, linea in enumerate(contenido_procesado):
    if i < primer_serie - 2 and linea.startswith('#'):
      linea = linea[1:]  # Elimina el primer carácter (el '#')
    resultado.append(linea)
  return resultado


def guardar_en_archivo(nuevo_contenido, nombre_archivo):
    """
    Args:
    el texto procesado y el nombre del archivo donde se almacenará el texto

    Returns:
    Nada (escribe en un archivo)
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        for linea in nuevo_contenido:
            archivo.write(linea + '\n')
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python plrm2wxr.py URL")
        sys.exit(1)

    url = re.sub(r"'\]", '', re.sub(r"\['", '', str(sys.argv[1:])))
    contenido_procesado = procesar_url(url)
    
    # Convertimos el contenido en una lista de líneas (si aún no lo está)
    lineas = contenido_procesado.splitlines()
    
    # Encontramos la primera línea que inicia con un número
    # Esta línea sería la primera serie de ejercicios
    primer_serie = encontrar_primera_serie(lineas)
    
    # Eliminamos los hashes hasta la línea indicada, es decir, 2 líneas antes que el primer set de ejercicios, para limpiar el texto libre que no es parte del entrenamiento
    nuevo_contenido = eliminar_hashes_hasta_linea(lineas, primer_serie)
    
    # Imprimir el contenido procesado en consola
    for linea in nuevo_contenido:
        print(linea)
    
    # Guardar el contenido en un archivo de texto
    guardar_en_archivo(nuevo_contenido, 'plrm2wxr.txt')
