import random
import json
import copy
from environment import Pokemon, Environment
from agents import BasicHeuristicAgent, AdvancedHeuristicAgent
from environment import TYPE_MULTIPLIERS  # <--- Ahora lo importa de aquí

# Parámetros del Algoritmo Genético "God Mode"
POPULATION_SIZE = 50      # Más cerebros compitiendo
GENERATIONS = 50          # Más tiempo para evolucionar
GAMES_PER_INDIVIDUAL = 20 # Más partidas para asegurar que ganan por habilidad, no por suerte
MUTATION_RATE = 0.15      # Reducimos un poco la mutación para que no pierdan lo aprendido

def load_team(filepath, num_pokemon=3):
    """Carga un equipo de Pokémon silenciosamente para el entrenamiento."""
    with open(filepath, 'r', encoding='utf-8') as f:
        roster = json.load(f)
    team_names = random.sample(list(roster.keys()), num_pokemon)
    team = [Pokemon({**roster[name], 'name': name}) for name in team_names]
    return team

def create_individual():
    """
    Cromosoma: Un diccionario de pesos.
    Genera 4 números aleatorios y los normaliza para que sumen 1.0.
    """
    weights = {
        'damage_score': random.random(),
        'speed_score': random.random(),
        'type_score': random.random(),
        'alive_score': random.random()
    }
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}

def calculate_fitness(individual, roster_path):
    """
    Fitness: Evalúa qué tan bueno es este conjunto de pesos.
    Hacemos pelear a un Nivel 3 (con estos pesos) vs Nivel 2.
    Devuelve la tasa de victorias (Win Rate) + un bono por HP restante.
    """
    wins = 0
    total_hp_bonus = 0.0

    for _ in range(GAMES_PER_INDIVIDUAL):
        team1 = load_team(roster_path)
        team2 = load_team(roster_path)
        
        # El evaluado usa los pesos del cromosoma
        agent_eval = AdvancedHeuristicAgent(player_id=1, weights=individual)
        # El oponente es el bot avaro básico (Nivel 2) de control
        agent_baseline = BasicHeuristicAgent(player_id=2)
        
        env = Environment(team1, team2)
        
        # Combate silencioso (sin prints)
        while env.check_win_condition() == 0:
            a1 = agent_eval.choose_action(env)
            a2 = agent_baseline.choose_action(env)
            env.execute_turn(a1, a2)
            
        if env.check_win_condition() == 1:
            wins += 1
            # Calcula el % de vida del equipo ganador como criterio de desempate
            my_team_hp = sum(p.current_hp for p in env.team1)
            my_team_max = sum(p.max_hp for p in env.team1)
            total_hp_bonus += (my_team_hp / my_team_max)

    # Fitness = Victorias principales + bono decimal por eficiencia
    fitness = wins + (total_hp_bonus / GAMES_PER_INDIVIDUAL)
    return fitness

def crossover(parent1, parent2):
    """Cruce: Promedia los pesos de los dos padres."""
    child = {}
    for key in parent1.keys():
        child[key] = (parent1[key] + parent2[key]) / 2.0
        
    # Normalizar de nuevo
    total = sum(child.values())
    return {k: v / total for k, v in child.items()}

def mutate(individual):
    """Mutación: Altera ligeramente un peso aleatorio."""
    if random.random() < MUTATION_RATE:
        key_to_mutate = random.choice(list(individual.keys()))
        # Modifica el peso agregando o restando hasta un 30%
        individual[key_to_mutate] += random.uniform(-0.3, 0.3)
        individual[key_to_mutate] = max(0.01, individual[key_to_mutate]) # Evitar negativos
        
        # Normalizar
        total = sum(individual.values())
        individual = {k: v / total for k, v in individual.items()}
    return individual

class Silenciador:
    """Clase dummy para atrapar y destruir los prints sin problemas de codificación."""
    def write(self, text):
        pass
    def flush(self):
        pass

def run_evolution(roster_path='data/pokemon_roster.json'):
    print("🧬 Iniciando Optimización Evolutiva (Algoritmo Genético) 🧬")
    print(f"Población: {POPULATION_SIZE} | Generaciones: {GENERATIONS}\n")
    
    # 1. Crear Población Inicial
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    
    import sys
    
    for generation in range(GENERATIONS):
        print(f"--- Entrenando Generación {generation + 1} ---")
        
        # 2. Evaluar Fitness
        # Silenciamos la consola de forma segura (evita errores de Emojis en Windows)
        old_stdout = sys.stdout
        sys.stdout = Silenciador()
        
        fitness_scores = [(ind, calculate_fitness(ind, roster_path)) for ind in population]
        
        # Restauramos la consola
        sys.stdout = old_stdout 
        
        # Ordenar de mejor a peor
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        best_ind, best_fitness = fitness_scores[0]
        print(f"🏆 Mejor Fitness de esta gen: {best_fitness:.2f} / {GAMES_PER_INDIVIDUAL}.00")
        print(f"📊 Pesos: {best_ind}\n")
        
        # 3. Selección y Cruce (Elitismo: conservamos a los 2 mejores)
        next_generation = [fitness_scores[0][0], fitness_scores[1][0]]
        
        while len(next_generation) < POPULATION_SIZE:
            # Selección por torneo (escogemos 3 al azar y nos quedamos con el mejor)
            tournament = random.sample(fitness_scores, 3)
            tournament.sort(key=lambda x: x[1], reverse=True)
            parent1 = tournament[0][0]
            
            tournament = random.sample(fitness_scores, 3)
            tournament.sort(key=lambda x: x[1], reverse=True)
            parent2 = tournament[0][0]
            
            # Cruzar y Mutar
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)
            
        population = next_generation
        
    print("==================================================")
    print("✅ ENTRENAMIENTO FINALIZADO ✅")
    print("Los pesos óptimos encontrados para ganar en Pokefisi son:")
    for k, v in best_ind.items():
        print(f" - {k}: {v:.4f}")
    print("==================================================")
    
    return best_ind

if __name__ == "__main__":
    run_evolution()