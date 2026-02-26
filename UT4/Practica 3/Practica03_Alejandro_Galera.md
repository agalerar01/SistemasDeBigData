# Práctica 03 – Clustering de Aptitudes Ninja con K-Means

## Objetivo

Aplicar el algoritmo **K-Means** para identificar grupos de ninjas según sus aptitudes:

* Fuerza física
* Control de chakra

Se utiliza el método del codo para determinar el número óptimo de clústeres.

---

# 1. Carga y Exploración de Datos

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Carga del dataset
df = pd.read_csv('aptitudes_ninja.csv')
print(df.head())

# Verificación de valores nulos
print("\n--- Buscamos nulos ---")
print(f"Fuerza fisica: {df['fuerza_fisica'].isnull().sum()}")
print(f"Control de Chakra: {df['control_chakra'].isnull().sum()}")

# Estadísticas descriptivas
print("\n--- Buscamos Valores Irreales ---")
print(df[['fuerza_fisica','control_chakra']].describe())
```

---

# 2. Método del Codo

Se prueba K desde 1 hasta 10 y se analiza la inercia.

```python
X = df[['fuerza_fisica', 'control_chakra']]

inercia = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inercia.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1, 11), inercia, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inercia')
plt.title('Método del Codo')
plt.xticks(range(1, 11))
plt.show()
```

 **Resultado:**
El “codo” se observa en **K = 4**, donde la reducción de la inercia deja de ser pronunciada.

---

# 3. Entrenamiento del Modelo Final

```python
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans_final.fit_predict(X)

print(df.head())
```

Cada ninja ahora tiene asignado un clúster.

---

# 4. Mapa de Especialidades

```python
plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x='fuerza_fisica',
    y='control_chakra',
    hue='cluster',
    palette='Set1',
    s=80
)

centroides = kmeans_final.cluster_centers_

plt.scatter(
    centroides[:, 0],
    centroides[:, 1],
    s=300,
    c='red',
    marker='X',
    label='Centroides'
)

plt.title('Mapa de Especialidades Ninja')
plt.xlabel('Fuerza Física')
plt.ylabel('Control de Chakra')
plt.legend()
plt.show()
```

Las “X” rojas representan los centroides de cada grupo.

---

# 5. Análisis de Perfiles

```python
centroides_df = pd.DataFrame(
    centroides,
    columns=['fuerza_fisica', 'control_chakra']
)

print(centroides_df)
```

Asignación de nombres:

```python
def asignar_nombre(fuerza, chakra):
    if fuerza > 70 and chakra > 70:
        return "Unidad Élite"
    elif fuerza > 70:
        return "Fuerza de Choque"
    elif chakra > 70:
        return "Unidad Médica"
    else:
        return "Exploradores"

centroides_df['especialidad'] = centroides_df.apply(
    lambda row: asignar_nombre(row['fuerza_fisica'], row['control_chakra']),
    axis=1
)

print(centroides_df)
```

---

# Conclusiones

* Se eligió **K = 4** porque el método del codo mostró un punto claro donde la disminución de la inercia cambia de pendiente.
* Los grupos encontrados representan perfiles diferenciados de ninjas:

  * **Unidad Élite:** Alta fuerza y alto control de chakra.
  * **Fuerza de Choque:** Alta fuerza física, menor control de chakra.
  * **Unidad Médica:** Alto control de chakra, menor fuerza física.
  * **Exploradores:** Niveles intermedios o bajos en ambas habilidades.

El algoritmo K-Means permitió segmentar correctamente a los ninjas en unidades estratégicas según sus habilidades predominantes.