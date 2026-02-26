import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1
df = pd.read_csv('misiones_limpias.csv')
stats = df['Nivel_Chakra'].describe()
print(stats)

media_chakra = stats['mean']
std_chakra = stats['std']

# 2
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['Nivel_Chakra'], color='orange')
plt.title('Analisis de Chakra')
plt.show()

# 3
df['Z_Score'] = (df['Nivel_Chakra'] - media_chakra) / std_chakra
infiltrados = df[df['Z_Score'].abs() > 3]

# 4
chakra_negativo = df[df['Nivel_Chakra'] < 0]
aldea_desconocida = df[df['Aldea'].str.lower() == 'desconocida']
super_ninjas = df[(df['Z_Score'].abs() > 2) & (df['Z_Score'].abs() <= 3)]

# 5
print("Infiltrados:")
print(infiltrados[['ID', 'Aldea', 'Nivel_Chakra', 'Z_Score']])

print(f"Chakra Negativo: {len(chakra_negativo)}")
print(f"Aldea Desconocida: {len(aldea_desconocida)}")
print(f"Super Ninjas: {len(super_ninjas)}")

if not infiltrados.empty and not aldea_desconocida.empty:
    coincidencia = infiltrados[infiltrados['ID'].isin(aldea_desconocida['ID'])]
    if not coincidencia.empty:
        print("Coincidencia detectada:")
        print(coincidencia)