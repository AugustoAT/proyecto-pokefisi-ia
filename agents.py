import random
import copy

# Matriz simplificada de ventajas ofensivas de tipo
TYPE_MULTIPLIERS = {
    "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0},
    "Poison": {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
    "Ground": {"Fire": 2.0, "Water": 1.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying": {"Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost": {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Dark": {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
    "Fairy": {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5}
}

class Agent:
    def __init__(self, player_id):
        self.player_id = player_id
    def choose_action(self, environment):
        raise NotImplementedError

class RandomAgent(Agent):
    def choose_action(self, environment):
        valid_actions = environment.get_valid_actions(self.player_id)
        return random.choice(valid_actions)

class BasicHeuristicAgent(Agent):
    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        opp_id = 2 if self.player_id == 1 else 1
        opp_pkmn = environment.get_active_pokemon(opp_id)
        best_move_idx = 0
        max_damage = -1
        
        print(f"\n[🧠 Nivel 2 Evaluando] Turno de {my_pkmn.name}")
        for i, move in enumerate(my_pkmn.moves):
            predicted_damage = environment.calculate_damage(my_pkmn, opp_pkmn, move)
            print(f"  -> {move['name']}: {predicted_damage} de daño proyectado.")
            if predicted_damage > max_damage:
                max_damage = predicted_damage
                best_move_idx = i
        return ('attack', best_move_idx)

class HumanAgent(Agent):
    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        valid_actions = environment.get_valid_actions(self.player_id)
        
        print(f"\n--- Tu Turno (Jugador {self.player_id}) ---")
        if my_pkmn.is_fainted():
            print(f"¡{my_pkmn.name} se ha debilitado! Debes enviar a otro Pokémon.")
        else:
            print(f"¿Qué debería hacer {my_pkmn.name}?")
            
        options = {}
        idx = 0
        
        # Filtramos y mostramos los ataques
        attacks = [a for a in valid_actions if a[0] == 'attack']
        if attacks:
            print("Ataques:")
            for a in attacks:
                move = my_pkmn.moves[a[1]]
                print(f"  [{idx}]: Usar {move['name']} (Poder: {move['power']}, Tipo: {move['type']})")
                options[idx] = a
                idx += 1
                
        # Filtramos y mostramos los cambios
        switches = [a for a in valid_actions if a[0] == 'switch']
        if switches:
            print("Cambios de Pokémon:")
            my_team = environment.team1 if self.player_id == 1 else environment.team2
            for s in switches:
                pkmn = my_team[s[1]]
                print(f"  [{idx}]: Cambiar a {pkmn.name} (HP: {pkmn.current_hp}/{pkmn.max_hp})")
                options[idx] = s
                idx += 1

        while True:
            try:
                choice = int(input(f"\nElige una opción (0-{idx-1}): "))
                if choice in options:
                    return options[choice]
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

class AdvancedHeuristicAgent(Agent):
    def __init__(self, player_id, weights=None):
        super().__init__(player_id)
        self.weights = weights if weights else {
            'damage_score': 0.4,
            'speed_score': 0.2,
            'type_score': 0.2,
            'alive_score': 0.2
        }

    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        opp_id = 2 if self.player_id == 1 else 1
        opp_pkmn = environment.get_active_pokemon(opp_id)
        valid_actions = environment.get_valid_actions(self.player_id)
        
        # Si estamos obligados a cambiar
        attacks = [a for a in valid_actions if a[0] == 'attack']
        if not attacks:
            return valid_actions[0] # Solo hay switches disponibles

        best_move_idx = 0
        best_score = -float('inf')

        print(f"\n[🧠 Nivel 3 Evaluando] Turno de {my_pkmn.name}")
        for a in attacks:
            i = a[1]
            move = my_pkmn.moves[i]
            score, details = self.evaluate_action(environment, my_pkmn, opp_pkmn, move)
            print(f"  -> {move['name']}: Puntaje Total = {score:.2f}")
            if score > best_score:
                best_score = score
                best_move_idx = i
                
        return ('attack', best_move_idx)

    def evaluate_action(self, env, my_pkmn, opp_pkmn, move):
        predicted_damage = env.calculate_damage(my_pkmn, opp_pkmn, move)
        damage_score = min(predicted_damage / opp_pkmn.max_hp, 1.0)

        total_speed = my_pkmn.speed + opp_pkmn.speed
        speed_score = my_pkmn.speed / total_speed if total_speed > 0 else 0.5

        move_type = move['type']
        multiplier = 1.0
        for t in opp_pkmn.types:
            multiplier *= TYPE_MULTIPLIERS.get(move_type, {}).get(t, 1.0)
        type_score = multiplier / 4.0

        my_team = env.team1 if self.player_id == 1 else env.team2
        opp_team = env.team2 if self.player_id == 1 else env.team1
        
        my_alive = sum(1 for p in my_team if not p.is_fainted()) / len(my_team)
        opp_alive = sum(1 for p in opp_team if not p.is_fainted()) / len(opp_team)
        
        if predicted_damage >= opp_pkmn.current_hp:
            opp_alive -= (1 / len(opp_team))
            
        alive_diff = my_alive - opp_alive
        alive_score = (alive_diff + 1) / 2

        total_score = (
            self.weights['damage_score'] * damage_score +
            self.weights['speed_score'] * speed_score +
            self.weights['type_score'] * type_score +
            self.weights['alive_score'] * alive_score
        )
        return total_score, {'dmg': damage_score, 'spd': speed_score, 'typ': type_score, 'alv': alive_score}

class MinimaxAgent(AdvancedHeuristicAgent):
    def __init__(self, player_id, depth=3, weights=None):
        super().__init__(player_id, weights)
        self.depth = depth # ¡Aprovechando que tu máquina es buena, Profundidad 3!

    def choose_action(self, environment):
        my_pkmn = environment.get_active_pokemon(self.player_id)
        valid_actions = environment.get_valid_actions(self.player_id)
        
        # Si solo queda 1 acción válida (ej. cambiar a la fuerza), no gastes CPU
        if len(valid_actions) == 1:
            return valid_actions[0]

        print(f"\n[🧠 Minimax Nivel 4] Explorando nodos de decisión (Profundidad {self.depth})...")
        best_score = -float('inf')
        best_action = valid_actions[0]

        # Explorar todas las acciones legales (Ataques y Cambios)
        for action in valid_actions:
            simulated_env = copy.deepcopy(environment)
            score = self.minimax(
                simulated_env, 
                depth=self.depth - 1, 
                alpha=-float('inf'), 
                beta=float('inf'), 
                is_maximizing=False,
                simulated_action=action
            )

            action_str = self._action_to_string(action, environment, self.player_id)
            print(f"  -> La opción [{action_str}] proyecta una utilidad futura de {score:.2f}")

            if score > best_score:
                best_score = score
                best_action = action

        final_str = self._action_to_string(best_action, environment, self.player_id)
        print(f"  => El MINIMAX se ha decidido por: {final_str}")
        return best_action
        
    def _action_to_string(self, action, env, player_id):
        """Auxiliar para imprimir lo que está pensando la IA"""
        if action[0] == 'attack':
            return env.get_active_pokemon(player_id).moves[action[1]]['name']
        else:
            team = env.team1 if player_id == 1 else env.team2
            return f"Relevar a {team[action[1]].name}"

    def minimax(self, env, depth, alpha, beta, is_maximizing, simulated_action=None):
        if depth == 0 or env.check_win_condition() != 0:
            return self.evaluate_state(env)

        my_id = self.player_id
        opp_id = 2 if my_id == 1 else 1

        if is_maximizing:
            max_eval = -float('inf')
            valid_actions = env.get_valid_actions(my_id)
            for action in valid_actions:
                sim_env = copy.deepcopy(env)
                eval = self.minimax(sim_env, depth - 1, alpha, beta, False, action)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            valid_actions = env.get_valid_actions(opp_id)
            for action in valid_actions:
                sim_env = copy.deepcopy(env)
                
                # Turno simultáneo simulado
                if simulated_action is not None:
                     action_p1 = simulated_action if my_id == 1 else action
                     action_p2 = action if my_id == 1 else simulated_action
                     sim_env.execute_turn(action_p1, action_p2)
                
                eval = self.minimax(sim_env, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_state(self, env):
        my_team = env.team1 if self.player_id == 1 else env.team2
        opp_team = env.team2 if self.player_id == 1 else env.team1

        my_total_hp = sum(p.current_hp for p in my_team)
        my_max_hp = sum(p.max_hp for p in my_team)
        opp_total_hp = sum(p.current_hp for p in opp_team)
        opp_max_hp = sum(p.max_hp for p in opp_team)
        
        my_hp_ratio = my_total_hp / my_max_hp if my_max_hp > 0 else 0
        opp_hp_ratio = opp_total_hp / opp_max_hp if opp_max_hp > 0 else 0
        hp_score = ((my_hp_ratio - opp_hp_ratio) + 1) / 2

        my_alive = sum(1 for p in my_team if not p.is_fainted()) / len(my_team)
        opp_alive = sum(1 for p in opp_team if not p.is_fainted()) / len(opp_team)
        alive_score = ((my_alive - opp_alive) + 1) / 2

        return (self.weights['damage_score'] * hp_score) + (self.weights['alive_score'] * alive_score)