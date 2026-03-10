import boto3

# Configuración inicial
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('CensoAlianza')

def actualizar_ninja_dinamicamente(id_ninja, fecha_registro, nivel):
    print(f"--- Actualizando registro {id_ninja} ---")
    
    try:
        respuesta = table.update_item(
            Key={
                'ID_Ninja': id_ninja,
                'Fecha_Registro': fecha_registro
            },
            # SET crea el atributo si no existe o lo actualiza si ya existe
            UpdateExpression="SET Nivel_Amenaza = :val",
            ExpressionAttributeValues={
                ':val': nivel
            },
            ReturnValues="UPDATED_NEW" # Nos devuelve solo lo que cambió
        )
        print(f"✅ Éxito. Atributos actualizados: {respuesta['Attributes']}")
    except Exception as e:
        print(f"❌ Error al actualizar: {e}")

# Llamada a la función (Asegúrate de que el ID y la Fecha coincidan con un registro real)
# Nota: La Fecha_Registro debe ser exactamente la que se guardó en el paso anterior.
actualizar_ninja_dinamicamente('N002', '2024-05-20T10:00:00.000000', 'S-Rank (Peligro Máximo)')