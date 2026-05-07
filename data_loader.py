import requests
import json
import random
import os

# URLs de los JSON compilados y limpios de Showdown
POKEDEX_URL = 'https://play.pokemonshowdown.com/data/pokedex.json'
MOVES_URL = 'https://play.pokemonshowdown.com/data/moves.json'
OUTPUT_FILE = 'data/pokemon_roster.json'

MAX_DEX_NUM = 386  # Límite hasta la 3ra Generación
ROSTER_SIZE = 30   # Cantidad de Pokémon requerida
MOVES_PER_PKMN = 8 # Cantidad de movimientos requerida

def generate_roster():
    print("Descargando JSON limpios desde los servidores de Showdown...")
    pokedex_raw = requests.get(POKEDEX_URL).json()
    moves_raw = requests.get(MOVES_URL).json()

    print("Filtrando Pokémon de Gen 1-3...")
    # Filtramos los Pokémon válidos de las primeras 3 generaciones
    valid_pokemon = [data for key, data in pokedex_raw.items() 
                     if data.get('num', 999) <= MAX_DEX_NUM and data.get('num') > 0]
    
    # Filtramos solo los movimientos que hacen daño real (vital para tu fórmula matemática)
    valid_moves = [data for key, data in moves_raw.items() 
                   if data.get('basePower', 0) > 0]

    selected_pokemon = random.sample(valid_pokemon, ROSTER_SIZE)
    roster = {}

    print(f"Procesando {ROSTER_SIZE} Pokémon...")
    for pkmn in selected_pokemon:
        pkmn_moves = random.sample(valid_moves, MOVES_PER_PKMN)
        
        roster[pkmn['name']] = {
            "id": pkmn['num'],
            "types": pkmn['types'],
            "stats": pkmn['baseStats'],
            "moves": [{
                "name": m['name'],
                "power": m['basePower'],
                "type": m['type'],
                "accuracy": m.get('accuracy', 100) if isinstance(m.get('accuracy'), int) else 100
            } for m in pkmn_moves]
        }

    os.makedirs('data', exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(roster, f, indent=4, ensure_ascii=False)
        
    print(f"\n¡Éxito! Tu roster ha sido guardado en {OUTPUT_FILE} de forma limpia.")

if __name__ == "__main__":
    generate_roster()