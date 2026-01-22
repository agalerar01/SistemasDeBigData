import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

print("Iniciando limpieza de Alejandro Galera...")

df = pd.read_csv("ventas_big.csv")

filas_iniciales = len(df)

df_sin_duplicados = df.drop_duplicates()
duplicados_eliminados = filas_iniciales - len(df_sin_duplicados)

cantidades_negativas = (df_sin_duplicados["cantidad"] < 0).sum()
df_sin_duplicados = df_sin_duplicados[df_sin_duplicados["cantidad"] >= 0]

def normalizar_producto(valor):
    if pd.isna(valor):
        return valor
    valor = valor.strip().lower()
    return valor.title().replace(" ", "")

df_sin_duplicados["producto"] = df_sin_duplicados["producto"].apply(normalizar_producto)

df_sin_duplicados["precio"] = pd.to_numeric(
    df_sin_duplicados["precio"], errors="coerce"
)

mediana_precio = df_sin_duplicados["precio"].median()
df_sin_duplicados["precio"].fillna(mediana_precio, inplace=True)

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

df_sin_duplicados["fecha"] = df_sin_duplicados["fecha"].apply(procesar_fecha)

archivo_salida = "ventas_limpias_Alejandro.json"
df_sin_duplicados.to_json(archivo_salida, orient="records", force_ascii=False, indent=4)

print("\n--- Bitácora de Limpieza ---")
print(f"Total de filas iniciales: {filas_iniciales}")
print(f"Filas eliminadas por duplicidad: {duplicados_eliminados}")
print(f"Mediana utilizada para precios: {mediana_precio}")
print(f"Registros con cantidades negativas descartados: {cantidades_negativas}")
print(f"Total de filas finales: {len(df_sin_duplicados)}")
print(f"Archivo generado: {archivo_salida}")
