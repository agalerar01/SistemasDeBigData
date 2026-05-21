# Centro de Inteligencia de la Alianza

**Informe Técnico · Lógica de Similitud y Especializaciones · REF-2025-SHN-07**

---

##  Resumen 

La aplicación es un sistema de exploración de talento futbolístico que, dado un jugador objetivo, identifica los cinco perfiles estadísticamente más similares dentro de una base de datos filtrada por edad y valor de mercado. Adicionalmente ofrece rastreo de promesas, visualización posicional y segmentación táctica automática.

| Parámetro | Valor |
|---|---|
| Métricas clave | 6 |
| Clones detectados | Top 5 |
| Clusters tácticos | 4 |

---

## 01 · Pipeline de análisis

**Flujo de procesamiento:** Carga CSV → Filtros sidebar → Normalización → Distancia → Ranking Top 5

Los datos se cargan una sola vez gracias a `@st.cache_data`, evitando lecturas repetidas en cada interacción del sidebar. El proceso es completamente estacionario: no hay aprendizaje incremental ni persistencia de estado entre sesiones.

---

## 02 · Preprocesamiento — Normalización Min-Max

Antes de calcular distancias, todas las métricas se reescalan al rango [0, 1] mediante `MinMaxScaler` de scikit-learn. Esto garantiza que variables con escalas muy distintas (como *xG* en décimas vs. *Pases_%* en porcentajes) contribuyan equitativamente al cálculo.

```
x_norm = (x − x_min) / (x_max − x_min)
```

Las seis métricas normalizadas son: `Goles`, `Asistencias`, `Pases_%`, `Regates`, `Recuperaciones`, `xG`.

---

## 03 · Motor de similitud — Distancia euclidiana en espacio 6D

El corazón del sistema calcula la distancia euclidiana entre el vector normalizado del jugador objetivo y cada candidato del conjunto filtrado. A menor distancia, mayor similitud estadística.

```
d(A, B) = √ Σ (a_i − b_i)²
          para i ∈ {Goles, Ast, Pases_%, Regates, Recup., xG}
```

Los resultados se ordenan de menor a mayor distancia y se devuelven los cinco primeros candidatos. El jugador objetivo queda excluido explícitamente del ranking mediante una comparación de nombre.

---

## 04 · Módulos especializados

###  Radar de inteligencia

Gráfico polar (`Plotly Scatterpolar`) del perfil normalizado del jugador objetivo. Permite lectura visual inmediata de fortalezas y debilidades relativas en las 6 métricas.

###  Rastreo de cantera

Filtra jugadores con `Edad ≤ 21` y `Potencial ≥ 80`. Opera sobre el dataframe original (no normalizado) para preservar los valores reales de potencial.

### Mapa de influencia

Scatter geoespacial (`Plotly Express`) usando coordenadas medias de actuación por jugador (`Coord_X_Media`, `Coord_Y_Media`), coloreado por equipo.

### Agrupamiento táctico

KMeans con `k=4` sobre las 6 métricas normalizadas. Asigna un cluster a cada jugador y los visualiza en un scatter Goles vs. Asistencias con color por grupo.

---

## 05 · Clusters tácticos — Segmentación KMeans (k = 4)

El algoritmo agrupa los jugadores en cuatro arquetipos tácticos según su perfil estadístico completo. La interpretación semántica de cada cluster debe realizarse a posteriori observando los centroides:

| Cluster | Arquetipo sugerido |
|---|---|
| C0 | Goleador puro |
| C1 | Creador de juego |
| C2 | Mediocampista completo |
| C3 | Perfil defensivo |

El parámetro `random_state=42` garantiza reproducibilidad entre ejecuciones.

---

## 06 · Evaluación crítica — Limitaciones del modelo

El sistema funciona correctamente como prototipo de exploración, pero presenta varios puntos de mejora:

- La búsqueda es O(n) lineal sobre el subconjunto filtrado: escalable, pero sin índice ANN para datasets grandes.
- La normalización sobre el conjunto completo puede generar sesgos si el filtro elimina los extremos estadísticos.
- No hay ponderación de métricas por posición táctica ni ajuste por minutos jugados.
- Los datos sintéticos del CSV de demostración no reflejan varianza real de mercado.

---