import requests
import json 

base_url = 'http://www.omdbapi.com/'
clave = ['82b3651d']

# Definir los parámetros de la búsqueda
parametros = {
    'apikey' : clave,
    't' : 'Memento'
}

# Enviar request a la API
response = requests.get(base_url, params=parametros)

# Comprobar si la solicitud fué exitosa (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Mostrar los datos
    print(data)
else: 
    # La solicitud no fué exitosa
    print('Request failed:', response.status_code)

titulo = data['Title']

