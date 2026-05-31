import requests
import json
import random
import os

# URLs de los JSON compilados limpios de Pokémon Showdown
POKEDEX_URL = "https://play.pokemonshowdown.com/data/pokedex.json"
MOVES_URL = "https://play.pokemonshowdown.com/data/moves.json"
OUTPUT_FILE = 'data/pokemon_roster.json'

TARGET_POKEMON = [
    "ivysaur", "venusaur", "charmeleon", "charizard", "machamp",
    "wartortle", "blastoise", "bayleef", "meganium", "magneton", "electabuzz", "magmar",
    "quilava", "typhlosion", "croconaw", "feraligatr", "magnezone", "electivire", "magmortar",
    "grovyle", "sceptile", "combusken", "blaziken", "absol", "dragonite", "tyranitar", "garchomp",
    "marshtomp", "swampert", "gengar", "snorlax", "gardevoir", "lucario", "kirlia", "umbreon"
]

MOVES_PER_PKMN = 8

def generate_roster():
    print("Descargando datos desde Pokémon Showdown...")
    pokedex_raw = requests.get(POKEDEX_URL).json()
    moves_raw = requests.get(MOVES_URL).json()

    print("Filtrando exclusivamente movimientos que hacen daño...")
    # Filtrar solo movimientos que hagan daño directo (power > 0)
    valid_moves = [data for key, data in moves_raw.items() if data.get("basePower", 0) > 0]

    pokemon_roster = {}

    print(f"Procesando tu lista estricta de {len(TARGET_POKEMON)} Pokémon...")
    for name in TARGET_POKEMON:
        if name in pokedex_raw:
            pkmn = pokedex_raw[name]
            
            # Asignar 8 movimientos aleatorios que hagan daño
            pkmn_moves = random.sample(valid_moves, MOVES_PER_PKMN)
            
            pokemon_roster[name] = {
                "id": pkmn.get('num'),
                "types": pkmn.get('types', []),
                "stats": pkmn.get('baseStats', {}),
                "moves": [{
                    "name": m['name'],
                    "power": m['basePower'],
                    "type": m['type'],
                    "accuracy": m.get('accuracy', 100) if isinstance(m.get('accuracy'), int) else 100
                } for m in pkmn_moves]
            }

    # Guardar localmente asegurando que la carpeta exista
    os.makedirs('data', exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(pokemon_roster, f, indent=4, ensure_ascii=False)
        
    print(f"\n¡Éxito! Tu roster exclusivo ha sido guardado en {OUTPUT_FILE}.")

if __name__ == "__main__":
    generate_roster()