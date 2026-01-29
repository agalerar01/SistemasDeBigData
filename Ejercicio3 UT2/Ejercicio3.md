# Práctica 3: Extracción de datos en CoinMarketCap

# Extracción de Datos de Criptomonedas desde CoinMarketCap con Python

## Objetivo del programa

Este script tiene como objetivo **conseguir información de criptomonedas** desde el sitio web *CoinMarketCap*, y guardarlos en un archivo CSV.
Se recopilan hasta **500 criptomonedas**, de estos se guardan:

* Nombre
* Símbolo
* Precio
* Capitalización de mercado (Market Cap)
* Volumen de negociación en 24 horas

---

## Librerías utilizadas

El programa hace uso de estas librerías de Python:

* **requests**: permite hacer solicitudes HTTP para conseguir el contenido de la página web.
* **BeautifulSoup (bs4)**: se utiliza para analizar y extraer información del código HTML.
* **pandas**: facilita la manipulación y almacenamiento de los datos en forma de tabla.
* **time**: se emplea para introducir pausas entre solicitudes y evitar bloqueos del servidor.

---

## Configuración inicial

```python
url_base = "https://coinmarketcap.com/?page={}"
headers = {
    'User-Agent': 'Mozilla/5.0 ...'
}
```

* `url_base` define la URL base del sitio, donde `{}` será reemplazado por el número de página.
* `headers` simula un navegador real mediante un *User-Agent* para evitar bloqueos por parte del sitio web.

---

## Función de limpieza de datos

```python
def limpiar_dato(texto):
```

Esta función:

* Elimina símbolos como `$`, `,` o letras.
* Conserva solo números, puntos y signos negativos.
* Convierte el valor resultante a tipo `float`.
* En caso de error o valor vacío, retorna `0.0`.

---

## Recolección de datos por páginas

```python
for i in range(1, 35):
```

* El bucle recorre las páginas 1 a 34 de CoinMarketCap.
* En cada iteración:

  * Se solicita el contenido HTML de la página.
  * Se analizan las filas (`<tr>`) de la tabla de criptomonedas.
  * Se extraen los datos relevantes de cada fila (`<td>`).

---

## Extracción de información clave

Para cada criptomoneda se obtienen:

* **Nombre**
* **Símbolo**
* **Precio**
* **Market Cap**
* **Volumen (24h)**

Estos datos se almacenan en una lista de diccionarios llamada `todas_las_criptos`.

---

## Control de límite y pausas

* El proceso se detiene automáticamente cuando se alcanzan **500 registros**.
* Se incluye una pausa de `2 segundos` entre páginas para evitar sobrecargar el servidor.

```python
time.sleep(2)
```

---

## Creación del DataFrame y exportación

```python
df = pd.DataFrame(todas_las_criptos)
df = df.drop_duplicates(subset=['Nombre', 'Símbolo']).head(500)
df.to_csv('cripto_data.csv', index=False, encoding='utf-8-sig')
```

* Los datos se convierten en un `DataFrame` de pandas.
* Se eliminan posibles duplicados.
* Se guardan los primeros 500 registros en un archivo CSV con codificación UTF-8.

---

## Resultado final

Al finalizar, el programa muestra un mensaje indicando el número total de registros guardados:

```python
¡Misión cumplida! Se han guardado 500 registros en 'cripto_data.csv'.
```

---

## Conclusión

Este programa demuestra el uso de **web scraping en Python**, combinando solicitudes HTTP, análisis de HTML y manipulación de datos para obtener información estructurada desde la web de manera automatizada.