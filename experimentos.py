import json
import random
import sys
import os
import csv
import time
from environment import Pokemon, Environment
from agents import RandomAgent, BasicHeuristicAgent, AdvancedHeuristicAgent, MinimaxAgent
from environment import TYPE_MULTIPLIERS  # <--- Ahora lo importa de aquí

# Parámetros del experimento
COMBATES_POR_ESCENARIO = 100 # Suficiente validez estadística
ROSTER_PATH = 'data/pokemon_roster.json'

class Silenciador:
    def write(self, text): pass
    def flush(self): pass

def load_team(filepath, num_pokemon=3):
    with open(filepath, 'r', encoding='utf-8') as f:
        roster = json.load(f)
    team_names = random.sample(list(roster.keys()), num_pokemon)
    return [Pokemon({**roster[name], 'name': name}) for name in team_names]

def ejecutar_escenario(nombre, agente1, agente2):
    print(f"\n🧪 Ejecutando: {nombre} ({COMBATES_POR_ESCENARIO} partidas)...")
    
    victorias_j1 = 0
    victorias_j2 = 0
    turnos_totales = 0
    
    # Silenciar prints de los agentes
    old_stdout = sys.stdout
    sys.stdout = Silenciador()
    
    start_time = time.time()
    
    for _ in range(COMBATES_POR_ESCENARIO):
        team1 = load_team(ROSTER_PATH)
        team2 = load_team(ROSTER_PATH)
        env = Environment(team1, team2)
        
        turnos = 0
        while env.check_win_condition() == 0:
            a1 = agente1.choose_action(env)
            a2 = agente2.choose_action(env)
            env.execute_turn(a1, a2)
            turnos += 1
            
            # Cortafuegos por si un escenario se alarga demasiado (ej. Minimax vs Minimax)
            if turnos > 150: 
                break
                
        ganador = env.check_win_condition()
        if ganador == 1: victorias_j1 += 1
        elif ganador == 2: victorias_j2 += 1
        turnos_totales += turnos

    # Restaurar consola
    sys.stdout = old_stdout
    end_time = time.time()
    
    win_rate_j1 = (victorias_j1 / COMBATES_POR_ESCENARIO) * 100
    win_rate_j2 = (victorias_j2 / COMBATES_POR_ESCENARIO) * 100
    avg_turnos = turnos_totales / COMBATES_POR_ESCENARIO
    tiempo_exec = end_time - start_time
    
    print(f"✅ Completado en {tiempo_exec:.2f} segundos.")
    return [nombre, win_rate_j1, win_rate_j2, avg_turnos, tiempo_exec]

if __name__ == "__main__":
    print("==================================================")
    print("📊 INICIANDO BATERÍA DE EXPERIMENTOS POKEFISI 📊")
    print("==================================================")
    
    # Usamos tus pesos evolucionados para el Nivel 3 y 4 (Reemplaza con los tuyos si los guardaste)
    pesos_optimos = {'damage_score': 0.2888, 'speed_score': 0.2357, 'type_score': 0.2008, 'alive_score': 0.2747}
    
    resultados = []
    
    # Escenario 1: Aleatorio vs Heurística Básica (El baseline)
    resultados.append(ejecutar_escenario(
        "Nivel 1 (Aleatorio) vs Nivel 2 (Básica)",
        RandomAgent(1), 
        BasicHeuristicAgent(2)
    ))
    
    # Escenario 2: Básica vs Avanzada
    resultados.append(ejecutar_escenario(
        "Nivel 2 (Básica) vs Nivel 3 (Avanzada)",
        BasicHeuristicAgent(1), 
        AdvancedHeuristicAgent(2, weights=pesos_optimos)
    ))
    
    # Escenario 3: Avanzada vs Minimax (Profundidad 2 para rapidez en el experimento)
    resultados.append(ejecutar_escenario(
        "Nivel 3 (Avanzada) vs Nivel 4 (Minimax Prof 2)",
        AdvancedHeuristicAgent(1, weights=pesos_optimos), 
        MinimaxAgent(2, depth=2, weights=pesos_optimos)
    ))
    
    # Guardar en CSV para tus gráficos de Excel
    csv_filename = "resultados_experimentos.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Escenario", "Win Rate J1 (%)", "Win Rate J2 (%)", "Promedio Turnos", "Tiempo (seg)"])
        writer.writerows(resultados)
        
    print("\n==================================================")
    print(f"📁 ¡Experimentos finalizados! Datos guardados en '{csv_filename}'.")
    for r in resultados:
        print(f"\n{r[0]}:")
        print(f"  - Gana J1: {r[1]}% | Gana J2: {r[2]}%")
        print(f"  - Turnos promedio: {r[3]:.1f}")