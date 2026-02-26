import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1
df = pd.read_csv('aptitudes_ninja.csv')
print(df.head())

# Nulos
print("\n--- Buscamos nulos ---")
print(f"Fuerza fisica: {df['fuerza_fisica'].isnull().sum()}")
print(f"Control de Chakra: {df['control_chakra'].isnull().sum()}")

# Valores Irreales
print("\n--- Buscamos Valores Irreales ---")
print(f"Fuerza fisica: {df['fuerza_fisica'].describe()}")
print(f"Control de Chakra: {df['control_chakra'].describe()}")


# 2 
X = df[['fuerza_fisica', 'control_chakra']]

inercia = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inercia.append(kmeans.inertia_)

# Graficamos
plt.figure(figsize=(8,5))
plt.plot(range(1, 11), inercia, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inercia')
plt.title('Método del Codo')
plt.xticks(range(1, 11))
plt.show()


# 3
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans_final.fit_predict(X)

print("\nPrimeros ninjas clasificados:")
print(df.head())

# 4
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

# 5
centroides_df = pd.DataFrame(
    centroides,
    columns=['fuerza_fisica', 'control_chakra']
)

print("\nCentroides:")
print(centroides_df)

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

print("\nEspecialidades asignadas:")
print(centroides_df)