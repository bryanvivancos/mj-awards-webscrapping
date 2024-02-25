# !pip install beautifulsoup4
# !pip install requests
# !pip install tqdm

# Hacer peticion HTTP
import requests
# Manipular código y guardar datos tabulares en archivo CSV
import pandas as pd
# Para evitar error: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version
from io import StringIO
#quitar espacios en numeros
from unicodedata import normalize
# Cargar o descargar archivos


# url de la página web a «escrapear»
url = 'https://es.wikipedia.org/wiki/Anexo:Premios_y_nominaciones_de_Michael_Jackson#Premios_Grammy'

# pasar "User-agent" para simular interacción con la página usando Navegador web
headers = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

respuesta = requests.get(url, headers=headers)

# El código de respuesta <200> indicará que todo salió bien
print(respuesta)

#busca todas las tablas que hay en la página
all_tables = pd.read_html(respuesta.content, encoding = 'utf8')
print(f'Total de tablas encontradas: {len(all_tables)}')

# StringIO Para evitar error: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version
matched_table = pd.read_html(StringIO(str(respuesta.text)), 
                             match='Mejor interpretación vocal contemporánea por un dúo, grupo o coro')

# imprime numero de tablas que coinciden con parametro match
print(f'Total de tablas encontradas: {len(matched_table)}')

# Guardar tabla en variable con nombre semántico
grammys_mj = matched_table[0]

# Verificamos si es la tabla que buscamos
print(grammys_mj.tail(2))

#Ahora asignaremos el AÑO como índice de la tabla.
grammys_mj.set_index('Año', inplace = True)

# Verificamos el cambio de índice
grammys_mj.head(2)

print(grammys_mj.head(2))

# Mostrar tipo de datos de la tabla
grammys_mj.dtypes

print(grammys_mj.dtypes)

#Como vemos, todos las columnas son de tipo de dato Objeto (lo que Pandas
# considera como una cadena de caracteres o String). Como Object es muy 
# amplio, necesitamos definir el tipo de dato correcto a cada columna para
# que luego se realizar operaciones con los datos.

# Creamos diccionario y pasamos múltiples columnas con el tipo de dato a asignar
convert_dict = {
    'Artista/Trabajo nominado': 'string',
    'Categoría': 'string',
    'Resultado': 'string'
}

grammys_mj = grammys_mj.astype(convert_dict)

# Verificamos que las columnas con números tengan el tipo de dato numérico asignado
print(grammys_mj.dtypes)

# Guarda Dataframe a archivo CSV
grammys_mj.to_csv('Output/premios_grammy_michael_jackson.csv')

# Leamos el archivo para verificar su creacion
pd.read_csv('premios_grammy_michael_jackson.csv').head(3)