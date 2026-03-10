from boto3.dynamodb.conditions import Key, Attr
import time
import boto3

# Configuración de la conexión
# Si corres esto localmente, asegúrate de tener configuradas tus credenciales de AWS
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Cambia la región si es necesario
table = dynamodb.Table('CensoAlianza')

# --- 1. QUERY (Buscando por ID_Ninja específico) ---
def ejecutar_query(id_ninja):
    print(f"\n--- Ejecutando QUERY para ID: {id_ninja} ---")
    inicio = time.perf_counter()
    
    # La Query requiere la Clave de Partición
    respuesta = table.query(
        KeyConditionExpression=Key('ID_Ninja').eq(id_ninja)
    )
    
    fin = time.perf_counter()
    print(f"Resultado: {respuesta['Items']}")

# --- 2. SCAN (Buscando por Clan - Atributo que no es clave) ---
def ejecutar_scan(clan):
    print(f"\n--- Ejecutando SCAN para Clan: {clan} ---")
    inicio = time.perf_counter()
    
    # El Scan revisa TODA la tabla y luego filtra
    respuesta = table.scan(
        FilterExpression=Attr('Clan').eq(clan)
    )
    
    fin = time.perf_counter()
    print(f"Resultado: {respuesta['Items']}")

# Pruebas
ejecutar_query('N001')
ejecutar_scan('Uchiha')