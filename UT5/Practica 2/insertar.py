import boto3
from datetime import datetime

# Configuración de la conexión
# Si corres esto localmente, asegúrate de tener configuradas tus credenciales de AWS
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Cambia la región si es necesario
table = dynamodb.Table('CensoAlianza')

# Datos de los Ninjas según los requerimientos del reto
ninjas = [
    # Ninja A: Nombre, Clan, Rango
    {
        'ID_Ninja': 'N001',
        'Fecha_Registro': datetime.now().isoformat(),
        'Nombre': 'Naruto Uzumaki',
        'Clan': 'Uzumaki',
        'Rango': 'Hokage'
    },
    {
        'ID_Ninja': 'N002',
        'Fecha_Registro': datetime.now().isoformat(),
        'Nombre': 'Sasuke Uchiha',
        'Clan': 'Uchiha',
        'Rango': 'Ninja Errante'
    },
    # Ninja B: Nombre, Habilidades_Especiales (Array), Herramientas (JSON/Map)
    {
        'ID_Ninja': 'N003',
        'Fecha_Registro': datetime.now().isoformat(),
        'Nombre': 'Kakashi Hatake',
        'Habilidades_Especiales': ['Chidori', 'Sharingan', 'Kamui'],
        'Herramientas': {
            'Principal': 'Kunai de espacio-tiempo',
            'Secundaria': 'Libro Icha Icha'
        }
    },
    # Ninja C: Nombre, Estado_Ultima_Mision
    {
        'ID_Ninja': 'N004',
        'Fecha_Registro': datetime.now().isoformat(),
        'Nombre': 'Shikamaru Nara',
        'Estado_Ultima_Mision': 'Completada con éxito'
    },
    {
        'ID_Ninja': 'N005',
        'Fecha_Registro': datetime.now().isoformat(),
        'Nombre': 'Sakura Haruno',
        'Estado_Ultima_Mision': 'En curso (Médico de apoyo)'
    }
]

def cargar_datos():
    print(f"Iniciando ingesta en tabla: {table.table_name}...")
    for ninja in ninjas:
        try:
            table.put_item(Item=ninja)
            print(f"✅ Registro insertado: {ninja['Nombre']} ({ninja['ID_Ninja']})")
        except Exception as e:
            print(f"❌ Error insertando {ninja['Nombre']}: {e}")

if __name__ == "__main__":
    cargar_datos()