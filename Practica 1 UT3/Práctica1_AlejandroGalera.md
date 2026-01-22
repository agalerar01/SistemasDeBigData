# Práctica 1: Hijo de la Forja

# Esta practica esta enfocada a hacer un script para limpieza de un csv(Limpieza de duplicados, tratamientos de precios, etc)

# Paso 1: Eliminacion de duplicados

```
df_sin_duplicados = df.drop_duplicates()
duplicados_eliminados = filas_iniciales - len(df_sin_duplicados)
```

# Paso 2: Normalización de productos

```
def normalizar_producto(valor):
    if pd.isna(valor):
        return valor
    valor = valor.strip().lower()
    return valor.title().replace(" ", "")
```

# Paso 3: Tratamiento de precios

```
mediana_precio = df_sin_duplicados["precio"].median()
df_sin_duplicados["precio"].fillna(mediana_precio, inplace=True)
```

# Paso 4: Validación de cantidades

```
cantidades_negativas = (df_sin_duplicados["cantidad"] < 0).sum()
df_sin_duplicados = df_sin_duplicados[df_sin_duplicados["cantidad"] >= 0]
```

# Paso 5: Estandarización temporal

```
def procesar_fecha(valor):
    if pd.isna(valor):
        return np.nan

    valor = str(valor).lower().strip()
    hoy = datetime.now()

    if valor == "ayer":
        return (hoy - timedelta(days=1)).date().isoformat()

    match = re.match(r"hace (\d+) dias?", valor)
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).date().isoformat()

    try:
        return pd.to_datetime(valor).date().isoformat()
    except:
        return np.nan
```

# Bitacora de Limpieza

![alt text](image.png)

# Preguntas de Reflexión

1. ¿Cuántos registros se perdieron en total tras todo el proceso de limpieza?

Se perdieron los registros eliminados por:

Duplicados exactos

Cantidades negativas

El total de registros perdidos:

filas_iniciales - filas_finales

2. ¿Hubo algún caso de id repetido con datos distintos? ¿Cómo se manejó?

Sí, el script no elimina automáticamente registros con el mismo id si otros campos son distintos.
Solo se eliminan duplicados cuando todos los campos son iguales.

3. ¿Por qué es más seguro usar la mediana que la media para imputar precios?

En datasets con errores humanos, la media puede distorsionarse fácilmente, mientras que la mediana refleja mejor el valor central real del mercado.

# Conclusion Final

La limpieza y normalización de los datos es muy importante antes de realizar cualquier análisis, sobre todo en entornos de Big Data donde se manejan grandes cantidades de información. Si los datos contienen errores, duplicados o formatos distintos, los resultados pueden ser poco fiables, aunque se utilicen herramientas muy potentes.