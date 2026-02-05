import pandas as pd

NOMBRE_AGENTE = "Alejandro Galera Rico"

try:
    df = pd.read_csv('registros_misiones.csv')
except FileNotFoundError:
    print("¡Error! El pergamino 'registros_misiones.csv' no ha sido encontrado.")
    exit()

# --- SECCIÓN 1: LIMPIEZA DE DATOS ---

def limpiar_registro(df):
    # Reto 1: Elimina filas duplicadas
    duplicados = df.duplicated().sum()
    print(f"--- [INFO] Se han detectado y eliminado {duplicados} clones (duplicados).")
    df = df.drop_duplicates()

    # Reto 2: Estandariza la columna 'aldea'
    df['aldea'] = df['aldea'].str.strip().str.capitalize()

    # Reto 3: Rellenar ninjas de Kiri anónimos
    mask_kiri = (df['nin_id'].isna()) & (df['aldea'] == 'Kiri')
    df.loc[mask_kiri, 'nin_id'] = 'Ninja de la Niebla Anonimo'

    # Reto 4: Convierte 'ts' a datetime
    df['ts'] = pd.to_datetime(df['ts'])

    # Reto 5: Filtra niveles de chakra imposibles
    # Asumimos que valores fuera de rango son errores de sensor y los eliminamos
    df = df[(df['chakra'] > 0) & (df['chakra'] <= 100000)]

    # Reto 6: Renombra las columnas
    df = df.rename(columns={
        'id_reg': 'ID',
        'ts': 'Fecha',
        'nin_id': 'Ninja',
        'status': 'Estado',
        'desc': 'Descripcion'
    })
    
    return df

# --- SECCIÓN 2: BÚSQUEDA Y CONSULTAS ---

def realizar_consultas(df):
    print("\n--- EJECUTANDO CONSULTAS DE INTELIGENCIA ---")

    # Reto 7: Palabras clave de amenaza
    amenazas = df[df['Descripcion'].str.contains('espía|sospechoso|enemigo', case=False, na=False)]
    print(f"\n> Amenazas detectadas ({len(amenazas)}):")
    print(amenazas[['ID', 'Ninja', 'Descripcion']].head())

    # Reto 8: Infiltrados de la Lluvia
    infiltrados_lluvia = df[(df['aldea'] == 'Amegakure') & (df['chakra'] > 5000) & (df['rango'] != 'D')]
    print("\n> Infiltrados potenciales de Amegakure (Chakra > 5000 y Rango alto):")
    print(infiltrados_lluvia)

    # Reto 9: Accesos de madrugada (23:00 a 05:00)
    # Usamos .dt.hour para extraer la hora
    madrugada = df[df['Fecha'].dt.hour.isin([23, 0, 1, 2, 3, 4, 5])]
    print(f"\n> Movimientos detectados en la madrugada: {len(madrugada)} registros.")

    # Reto 10: Top 5 ninjas con más chakra por aldea
    top_chakra = df.sort_values(['aldea', 'chakra'], ascending=[True, False]).groupby('aldea').head(5)
    print("\n> Elite de las Aldeas (Top 5 Chakra):")
    print(top_chakra[['aldea', 'Ninja', 'chakra']])

    # Reto 11: Ninjas fuera de la Alianza (Konoha, Suna, Kumo)
    alianza = ['Konoha', 'Suna', 'Kumo']
    extranjeros = df[~df['aldea'].isin(alianza)]
    print(f"\n> Registros de ninjas ajenos a la Alianza: {len(extranjeros)}")

    # Reto 12: Misiones fallidas por aldea
    fallos_por_aldea = df[df['Estado'] == 'Fallo'].groupby('aldea').size()
    print("\n> Mapa de Fallos por Aldea:")
    print(fallos_por_aldea)

print(f"Iniciando Rastreo de Chakra de {NOMBRE_AGENTE}...")

df_limpio = limpiar_registro(df)
realizar_consultas(df_limpio)

nombre_salida = f'misiones_limpias_{NOMBRE_AGENTE.replace(" ", "_")}.csv'
df_limpio.to_csv(nombre_salida, index=False)
print(f"\n[MISIÓN CUMPLIDA] Archivo guardado como: {nombre_salida}")