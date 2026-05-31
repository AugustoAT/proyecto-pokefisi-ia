import json
import random
from environment import Pokemon, Environment
from agents import RandomAgent, BasicHeuristicAgent, HumanAgent, AdvancedHeuristicAgent, MinimaxAgent, TYPE_MULTIPLIERS

def load_team(filepath, num_pokemon=3):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            roster = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {filepath}.")
        exit()
        
    team_names = random.sample(list(roster.keys()), num_pokemon)
    team = []
    for name in team_names:
        pkmn_data = roster[name]
        pkmn_data['name'] = name 
        team.append(Pokemon(pkmn_data))
    return team

def check_effectiveness(move_type, defender_types):
    multiplier = 1.0
    for t in defender_types:
        multiplier *= TYPE_MULTIPLIERS.get(move_type, {}).get(t, 1.0)
    
    if multiplier >= 2.0:
        return "¡Es SÚPER efectivo!"
    elif multiplier == 0.0:
        return "No tiene ningún efecto..."
    elif multiplier <= 0.5:
        return "No es muy efectivo..."
    return ""

def run_battle(agent1, agent2, team1, team2, is_interactive=False):
    env = Environment(team1, team2)
    print("\n" + "="*50)
    print("🥊 ¡COMIENZA EL COMBATE POKEFISI! 🥊")
    print("="*50)
    
    turn = 1
    while env.check_win_condition() == 0:
        print(f"\n" + "-"*20 + f" Turno {turn} " + "-"*20)
        p1_active = env.get_active_pokemon(1)
        p2_active = env.get_active_pokemon(2)
        
        print(f"J1: {p1_active.name} [HP: {p1_active.current_hp}/{p1_active.max_hp}] (Tipos: {', '.join(p1_active.types)})")
        print(f"J2: {p2_active.name} [HP: {p2_active.current_hp}/{p2_active.max_hp}] (Tipos: {', '.join(p2_active.types)})")

        action1 = agent1.choose_action(env)
        action2 = agent2.choose_action(env)

        print("\n[⚔️ Resolución del Turno]")
        # 1. Narrar los cambios si ocurrieron
        if action1[0] == 'switch':
            print(f"> 🔄 J1 retiró a {p1_active.name} y envió a {env.team1[action1[1]].name}!")
        if action2[0] == 'switch':
            print(f"> 🔄 J2 (IA) retiró a {p2_active.name} y envió a {env.team2[action2[1]].name}!")

        # 2. Ejecutar lógicas de daño en el entorno
        env.execute_turn(action1, action2)

        # 3. Narrar los ataques verificando quién está vivo ahora en el campo
        p1_active_new = env.get_active_pokemon(1)
        p2_active_new = env.get_active_pokemon(2)

        if action1[0] == 'attack' and not p1_active.is_fainted():
            move = p1_active.moves[action1[1]]
            print(f"> 💥 {p1_active.name} usó {move['name']}.")
            eff = check_effectiveness(move['type'], p2_active_new.types)
            if eff: print(f"  {eff}")
            
        if action2[0] == 'attack' and not p2_active.is_fainted():
            move = p2_active.moves[action2[1]]
            print(f"> 💥 {p2_active.name} usó {move['name']}.")
            eff = check_effectiveness(move['type'], p1_active_new.types)
            if eff: print(f"  {eff}")

        if p1_active_new.is_fainted():
            print(f"\n💀 ¡El {p1_active_new.name} del Jugador 1 se ha debilitado!")
        if p2_active_new.is_fainted():
            print(f"\n💀 ¡El {p2_active_new.name} del Jugador 2 se ha debilitado!")
            
        turn += 1
        
        if is_interactive and env.check_win_condition() == 0:
            input("\n[Presiona ENTER para ir al siguiente turno...]")

    winner = env.check_win_condition()
    agent_name = "Jugador 1" if winner == 1 else "Jugador 2 (IA Minimax)"
    print("\n" + "="*50)
    print(f"🏆 ¡EL COMBATE HA TERMINADO!")
    print(f"🏆 ¡El ganador es el {agent_name}!")
    print("="*50 + "\n")

if __name__ == "__main__":
    print("Cargando base de datos de Pokémon...")
    equipo1 = load_team('data/pokemon_roster.json')
    equipo2 = load_team('data/pokemon_roster.json')
    
    print("\n" + "="*40)
    print(" MENÚ DE SELECCIÓN POKEFISI ")
    print("="*40)
    print("1. Máquina vs Máquina (Heurística Nivel 3 vs MINIMAX Nivel 4)")
    print("2. Humano vs Máquina (Tú vs MINIMAX Nivel 4)")
    
    while True:
        modo = input("\nIngresa 1 o 2 para elegir el modo de juego: ")
        
        if modo == "1":
            jugador1 = AdvancedHeuristicAgent(player_id=1)
            is_interactive = True 
            break
        elif modo == "2":
            jugador1 = HumanAgent(player_id=1)
            is_interactive = True
            break
        else:
            print("❌ Opción no válida. Por favor, ingresa 1 o 2.")

# Reemplaza estos valores con los que te arroje tu mega-entrenamiento
    pesos_evolucionados = {
        'damage_score': 0.3294,
        'speed_score': 0.2101,
        'type_score': 0.1917,
        'alive_score': 0.2689
    }

    # MINIMAX a Profundidad 3 armado con los Pesos Genéticos
    jugador2 = MinimaxAgent(player_id=2, depth=3, weights=pesos_evolucionados)

    run_battle(jugador1, jugador2, equipo1, equipo2, is_interactive=is_interactive)