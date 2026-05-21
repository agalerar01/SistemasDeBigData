import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance
from sklearn.cluster import KMeans

import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Centro de Inteligencia Shinobi",
    layout="wide",
    page_icon="🏯"
)

st.markdown("""
<style>

.main {
    background-color: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #161b22;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():

    import os

    ruta = os.path.join(
        os.path.dirname(__file__),
        "players_data.csv"
    )

    df = pd.read_csv(ruta)

    return df

df = cargar_datos()

metricas = [
    "Goles",
    "Asistencias",
    "Pases_%",
    "Regates",
    "Recuperaciones",
    "xG"
]

scaler = MinMaxScaler()

df_normalizado = df.copy()

df_normalizado[metricas] = scaler.fit_transform(
    df[metricas]
)

st.sidebar.title("⚙️ Panel de Inteligencia")

jugador_objetivo = st.sidebar.selectbox(
    "Selecciona el jugador objetivo",
    df["Nombre"]
)

edad_max = st.sidebar.slider(
    "Edad máxima",
    16,
    40,
    30
)

valor_max = st.sidebar.slider(
    "Valor máximo de mercado",
    int(df["Valor_Mercado"].min()),
    int(df["Valor_Mercado"].max()),
    int(df["Valor_Mercado"].max())
)

df_filtrado = df_normalizado[
    (df_normalizado["Edad"] <= edad_max) &
    (df_normalizado["Valor_Mercado"] <= valor_max)
]

objetivo = df_filtrado[
    df_filtrado["Nombre"] == jugador_objetivo
]

if objetivo.empty:
    st.error("El jugador no cumple los filtros.")
    st.stop()

vector_objetivo = objetivo[metricas].values[0]

distancias = []

for index, row in df_filtrado.iterrows():

    if row["Nombre"] != jugador_objetivo:

        vector_candidato = row[metricas].values

        dist = distance.euclidean(
            vector_objetivo,
            vector_candidato
        )

        distancias.append((row["Nombre"], dist))

similares = sorted(
    distancias,
    key=lambda x: x[1]
)[:5]

df_similares = pd.DataFrame(
    similares,
    columns=["Jugador", "Distancia"]
)

st.title(" Centro de Inteligencia de la Alianza")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jugadores Analizados", len(df_filtrado))

with col2:
    st.metric("Jugador Objetivo", jugador_objetivo)

with col3:
    st.metric("Similitud Detectada", "Top 5")

# ---------------------------------------------------
# TABLA DE SIMILARES
# ---------------------------------------------------

st.subheader(" Clones Estadísticos Detectados")

st.dataframe(df_similares)

st.subheader(" Radar de Inteligencia")

categorias = metricas

valores = objetivo[metricas].values[0].tolist()

valores += valores[:1]
categorias += categorias[:1]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=valores,
    theta=categorias,
    fill='toself',
    name=jugador_objetivo
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0,1]
        )
    ),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

st.subheader(" Rastreo de Cantera")

promesas = df[
    (df["Edad"] <= 21) &
    (df["Potencial"] >= 80)
]

st.dataframe(
    promesas[
        ["Nombre", "Edad", "Potencial"]
    ]
)
    
st.subheader(" Mapa de Influencia")

fig_mapa = px.scatter(
    df,
    x="Coord_X_Media",
    y="Coord_Y_Media",
    color="Equipo",
    hover_name="Nombre"
)

st.plotly_chart(
    fig_mapa,
    use_container_width=True
)

st.subheader(" Agrupamiento Táctico")

kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

df["Cluster"] = kmeans.fit_predict(
    df_normalizado[metricas]
)

fig_cluster = px.scatter(
    df,
    x="Goles",
    y="Asistencias",
    color=df["Cluster"].astype(str),
    hover_name="Nombre"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

with st.expander(" Ver Explicación del Modelo"):

    st.write("""
    La aplicación utiliza distancia euclidiana
    sobre métricas normalizadas para encontrar
    perfiles estadísticamente similares.
    """)