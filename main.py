import json
import random
from environment import Pokemon, Environment
from agents import RandomAgent, BasicHeuristicAgent, HumanAgent # Importamos el HumanAgent

def load_team(filepath, num_pokemon=3):
    """Carga un equipo de Pokémon desde el JSON limpio."""
    with open(filepath, 'r', encoding='utf-8') as f:
        roster = json.load(f)
    
    team_names = random.sample(list(roster.keys()), num_pokemon)
    team = []
    for name in team_names:
        pkmn_data = roster[name]
        pkmn_data['name'] = name 
        team.append(Pokemon(pkmn_data))
    return team

def run_battle(agent1, agent2, team1, team2):
    """Ejecuta la simulación interactiva del combate."""
    env = Environment(team1, team2)
    print("\n" + "="*40)
    print("¡COMIENZA EL COMBATE POKEFISI INTERACTIVO!")
    print("="*40)
    
    turn = 1
    while env.check_win_condition() == 0:
        print(f"\n" + "-"*15 + f" Turno {turn} " + "-"*15)
        p1_active = env.get_active_pokemon(1)
        p2_active = env.get_active_pokemon(2)
        
        print(f"J1 (TÚ): {p1_active.name} [HP: {p1_active.current_hp}/{p1_active.max_hp}]")
        print(f"J2 (CPU): {p2_active.name} [HP: {p2_active.current_hp}/{p2_active.max_hp}]")

        # Los agentes deciden qué hacer
        action1 = agent1.choose_action(env)
        action2 = agent2.choose_action(env)

        # Capturamos HP antes del turno para mostrar el daño
        hp_p1_before = p1_active.current_hp
        hp_p2_before = p2_active.current_hp

        # El entorno ejecuta el turno
        env.execute_turn(action1, action2)

        # Imprimimos resumen de daño
        dmg_to_p2 = hp_p2_before - p2_active.current_hp
        dmg_to_p1 = hp_p1_before - p1_active.current_hp
        print(f"\n> Tu {p1_active.name} usó su ataque e hizo {dmg_to_p2} de daño.")
        print(f"> El {p2_active.name} enemigo atacó e hizo {dmg_to_p1} de daño.")

        if p1_active.is_fainted():
            print(f"\n¡Tu {p1_active.name} se ha debilitado!")
            env.active_idx_1 += 1
        if p2_active.is_fainted():
            print(f"\n¡El {p2_active.name} enemigo se ha debilitado!")
            env.active_idx_2 += 1
            
        turn += 1
        
        # Pausa dramática para que el usuario pueda leer
        if env.check_win_condition() == 0:
            input("\n[Presiona ENTER para ir al siguiente turno...]")

    winner = env.check_win_condition()
    agent_name = "Jugador 1 (Humano)" if winner == 1 else "Jugador 2 (CPU Heurística)"
    print("\n" + "="*40)
    print(f"¡EL COMBATE HA TERMINADO!")
    print(f"¡El ganador es el {agent_name}!")
    print("="*40 + "\n")

if __name__ == "__main__":
    print("Cargando base de datos...")
    equipo1 = load_team('data/pokemon_roster.json')
    equipo2 = load_team('data/pokemon_roster.json')

    # CAMBIO: Jugador 1 ahora eres tú (HumanAgent), Jugador 2 es la CPU (Heurística)
    jugador1 = HumanAgent(player_id=1)
    jugador2 = BasicHeuristicAgent(player_id=2)

    run_battle(jugador1, jugador2, equipo1, equipo2)