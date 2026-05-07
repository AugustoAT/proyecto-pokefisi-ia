import random

class Agent:
    """Clase base para todos los agentes (útil para tu arquitectura futura)."""
    def __init__(self, player_id):
        self.player_id = player_id

    def choose_action(self, environment):
        raise NotImplementedError

class RandomAgent(Agent):
    """
    Agente Nivel 1: Comportamiento Aleatorio.
    Selecciona acciones sin criterio (baseline) según la rúbrica.
    """
    def choose_action(self, environment):
        # Elige un ataque al azar entre los 4 disponibles (índices 0 a 3)
        return random.randint(0, 3)

class BasicHeuristicAgent(Agent):
    """
    Agente Nivel 2: Heurística Básica.
    Función basada en la diferencia de HP. Busca maximizar el daño 
    para aumentar la brecha de HP a su favor.
    """
    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        opp_id = 2 if self.player_id == 1 else 1
        opp_pkmn = environment.get_active_pokemon(opp_id)

        best_move_idx = 0
        max_damage = -1

        # Simula los 4 ataques disponibles y elige el que más daño hace
        # Esto maximiza la diferencia de HP a favor del agente
        for i, move in enumerate(my_pkmn.moves):
            predicted_damage = environment.calculate_damage(my_pkmn, opp_pkmn, move)
            if predicted_damage > max_damage:
                max_damage = predicted_damage
                best_move_idx = i
        
        return best_move_idx

class HumanAgent(Agent):
    """
    Agente controlado por el usuario por consola.
    Permite cumplir el requisito de 'humano vs máquina'.
    """
    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        print(f"\n--- Tu Turno ---")
        print(f"¿Qué debería hacer {my_pkmn.name}?")
        
        # Muestra las opciones de ataques
        for i, move in enumerate(my_pkmn.moves):
            print(f"  [{i}]: {move['name']} (Poder: {move['power']}, Tipo: {move['type']})")

        # Bucle para asegurar que el usuario ingrese una opción válida
        while True:
            try:
                choice = int(input("\nElige el número de tu movimiento (0-3): "))
                if 0 <= choice <= 3:
                    return choice
                else:
                    print("Por favor, elige un número del 0 al 3.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")