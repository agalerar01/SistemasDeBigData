import requests
import pandas as pd
import time

url = "https://pokeapi.co/api/v2/pokemon?limit=20"

pokemon_detalles = []

print("Iniciando extracción de Pokémon...\n")

contador = 1

while url:
    response = requests.get(url)
    data = response.json()

    for pokemon in data["results"]:
        detalle_response = requests.get(pokemon["url"])
        detalle = detalle_response.json()

        info = {
            "name": detalle["name"],
            "height": detalle["height"],
            "weight": detalle["weight"],
            "base_experience": detalle["base_experience"]
        }

        pokemon_detalles.append(info)

        print(
            f"{contador}. Pokémon cargado → "
            f"Nombre: {info['name']} | "
            f"Altura: {info['height']} | "
            f"Peso: {info['weight']} | "
            f"Experiencia base: {info['base_experience']}"
        )

        contador += 1
        time.sleep(0.2)

    url = data["next"]

df = pd.DataFrame(pokemon_detalles)

df["height_m"] = df["height"] / 10
df["weight_kg"] = df["weight"] / 10
df["bmi"] = df["weight_kg"] / (df["height_m"] ** 2)

df.to_csv("pokemon_limpio.csv", index=False)

print("\nArchivo pokemon_limpio.csv generado correctamente ✅")
