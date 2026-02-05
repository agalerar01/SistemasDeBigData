¡Misión cumplida, Jōnin! Aquí tienes el archivo Markdown estructurado y listo para que lo copies, pegues en tu repositorio y solo rellenes tus datos personales y las capturas de pantalla.

He mantenido el tono de la división de inteligencia ANBU para que tu informe destaque en los archivos de la Hoja.

---

# Practica 1: El Rastro de la Grieta

**Misión de Restauración del Pergamino Digital**

## 🛡️ Descripción de la Misión

Los registros de la Puerta Principal fueron saboteados por espías. La misión consistió en implementar un sistema de análisis utilizando la librería **Pandas** para limpiar, normalizar y extraer inteligencia crítica de un dataset de 1,500 registros. El objetivo final: localizar infiltrados de **Amegakure** y asegurar la integridad de la base de datos de misiones.

---

## 📂 Evidencias del Protocolo de Limpieza

### Bloque A: Limpieza de Datos (Función `limpiar_registro`)

En esta fase se eliminaron duplicados (clones), se normalizaron los nombres de las aldeas y se gestionaron los valores nulos en la región de la Niebla.

```python
def limpiar_registro(df):
    # 1. Eliminación de Clones
    df = df.drop_duplicates()

    # 2. Estandarización de Aldeas (Normalización)
    df['aldea'] = df['aldea'].str.strip().str.capitalize()

    # 3. Identidad en la Niebla (Gestión de Nulos)
    mask_kiri = (df['nin_id'].isna()) & (df['aldea'] == 'Kiri')
    df.loc[mask_kiri, 'nin_id'] = 'Ninja de la Niebla Anonimo'

    # 4. Despertar de la Fecha (Conversión a datetime)
    df['ts'] = pd.to_datetime(df['ts'])

    # 5. Control de Chakra (Filtro de valores imposibles)
    df = df[(df['chakra'] > 0) & (df['chakra'] <= 100000)]

    # 6. Formato ANBU (Renombrar columnas)
    df = df.rename(columns={
        'id_reg': 'ID',
        'ts': 'Fecha',
        'nin_id': 'Ninja',
        'status': 'Estado',
        'desc': 'Descripcion'
    })
    return df

```

### Bloque B: Búsqueda y Consultas Avanzadas (Función `realizar_consultas`)

Extracción de inteligencia táctica para identificar amenazas y movimientos sospechosos.

```python
def realizar_consultas(df):
    # Reto 7: Palabras Clave (Detección de Amenazas)
    amenazas = df[df['Descripcion'].str.contains('espía|sospechoso|enemigo', case=False, na=False)]
    
    # Reto 8: El Infiltrado de la Lluvia
    infiltrados = df[(df['aldea'] == 'Amegakure') & (df['chakra'] > 5000) & (df['rango'] != 'D')]
    
    # Reto 9: Vigilancia Nocturna (23:00 - 05:00)
    madrugada = df[df['Fecha'].dt.hour.isin([23, 0, 1, 2, 3, 4, 5])]
    
    # Reto 10: La Elite de las Aldeas (Top 5 Chakra)
    top_chakra = df.sort_values(['aldea', 'chakra'], ascending=[True, False]).groupby('aldea').head(5)
    
    # Reto 11: Rastreo de Extranjeros (Fuera de la Alianza)
    alianza = ['Konoha', 'Suna', 'Kumo']
    extranjeros = df[~df['aldea'].isin(alianza)]
    
    # Reto 12: Mapa de Fallos
    fallos_por_aldea = df[df['Estado'] == 'Fallo'].groupby('aldea').size()

```

---

## 📸 Resultados en Consola

*(Inserta aquí tus capturas de pantalla de los prints ejecutados)*

> **Nota del Agente:** [Aquí debes colocar la captura de pantalla donde se vea el inicio del rastreo con tu nombre y los resultados de las tablas filtradas].

---

## 🧠 Preguntas de Reflexión

**1. ¿Cuántos registros duplicados has encontrado y qué impacto tendrían en un análisis de Big Data si no se eliminaran?**

* **Respuesta:** (Menciona aquí el número que te salió en el script). En un entorno de Big Data, los duplicados sesgan los resultados, provocando que los comandantes tomen decisiones basadas en datos inflados. Podríamos enviar refuerzos a una zona donde no hay nadie, solo porque un registro se repitió mil veces.

**2. ¿Por qué es crítico convertir la columna de fecha a `datetime` antes de realizar búsquedas por franja horaria?**

* **Respuesta:** Porque como texto, la fecha es solo una cadena de caracteres sin significado lógico. Al convertirla a `datetime`, Pandas activa su "ojo de la mente", permitiéndonos extraer componentes como la hora, el día o el mes de forma instantánea para detectar patrullas nocturnas.

**3. ¿Cómo has manejado los niveles de chakra > 100,000? ¿Crees que son errores de sensor o posibles técnicas prohibidas?**

* **Respuesta:** Los he filtrado fuera del análisis. Si bien podrían ser Jinchūrikis usando técnicas prohibidas, estadísticamente es más probable que sean fallos en los sensores de la puerta causados por interferencias electromagnéticas o sabotaje enemigo.

---

## 🏁 Conclusión

Pandas es el arma definitiva para un analista ANBU. Mientras que un ninja rastreador tardaría horas en revisar un pergamino de 1,500 líneas buscando patrones a mano, un script bien diseñado permite **limpiar, normalizar y detectar amenazas en milisegundos**. La eficiencia tecnológica no reemplaza al instinto ninja, pero le da una ventaja táctica inalcanzable.

---

**Iniciando Rastreo de Chakra de: [Tu Nombre y Apellidos]**
**Archivo generado:** `misiones_limpias_[TuNombre].csv`

---

¿Hay algún otro detalle técnico o "jutsu" de programación que necesites añadir antes de entregar tu reporte? Sería un placer ayudarte a pulirlo.