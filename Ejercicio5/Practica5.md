# 1. Diseño y Creación de la Tabla

Partition Key: SensorID
Sort Key: Timestamp

![alt text](image.png)

# 2. Ingesta de Datos (Create)

Voy a insertar 2 sensores distintos que tengan 3 mediciones cada uno

![alt text](image-1.png)

# 3. Consulta de Datos

Vamos a ver como evoluciona el sensor de temperatura de la zona Norte 01

![alt text](image-2.png)

Con la linea --scan-index-forward hace que se ordene de la mas reciente a la mas antigua

# 4. Actualización de Datos

Los datos antes de hacer el update 
![alt text](image-3.png)

El codigo utilizado en CLI
![alt text](image-4.png)

Los datos una vez hecho el update
![alt text](image-5.png)

# 5. Eliminación de Datos

La tabla antes de hacer el detele
![alt text](image-6.png)

El codigo utilizado en CLI
![alt text](image-7.png)

La tabla despues de hacer el delete
![alt text](image-8.png)

# Conclusion

Es util para los datos de los sensores ya que puede almacenar mucha informacion sin realentizarse.
Se pueden consultar facil y rapido los datos y podemos crear un indice especial para hacer busquedas concretas. Es una buena herramienta para trabajar con proyectos de IoT