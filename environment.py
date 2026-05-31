import random

class Pokemon:
    def __init__(self, data_dict):
        """Inicializa un Pokémon usando el diccionario del JSON."""
        self.name = data_dict["name"] 
        self.types = data_dict["types"]
        
        # Atributos clave corregidos para leer el formato de Showdown ('atk', 'def', 'spe')
        self.max_hp = data_dict["stats"]["hp"]
        self.current_hp = self.max_hp
        self.attack = data_dict["stats"]["atk"]
        self.defense = data_dict["stats"]["def"]
        self.speed = data_dict["stats"]["spe"]
        
        # Selección aleatoria de 4 movimientos de los 8 disponibles
        self.moves = random.sample(data_dict["moves"], 4)
        
    def is_fainted(self):
        """Verifica si el Pokémon tiene 0 HP."""
        return self.current_hp <= 0

    def take_damage(self, damage):
        """Aplica el daño asegurando que el HP no baje de 0."""
        self.current_hp = max(0, self.current_hp - damage)


class Environment:
    def __init__(self, team1, team2, k_factor=0.5):
        self.team1 = team1
        self.team2 = team2
        self.k = k_factor
        self.active_idx_1 = 0
        self.active_idx_2 = 0

    def get_active_pokemon(self, player):
        if player == 1:
            return self.team1[self.active_idx_1]
        return self.team2[self.active_idx_2]

    def get_valid_actions(self, player_id):
        """Genera todas las acciones legales para un jugador: ataques y cambios."""
        actions = []
        active_pkmn = self.get_active_pokemon(player_id)
        
        # 1. Acciones de ataque (solo si tiene HP)
        if not active_pkmn.is_fainted():
            for i in range(len(active_pkmn.moves)):
                actions.append(('attack', i))
            
        # 2. Acciones de cambio (hacia pokemon vivos en la banca)
        team = self.team1 if player_id == 1 else self.team2
        active_idx = self.active_idx_1 if player_id == 1 else self.active_idx_2
        
        for i, pkmn in enumerate(team):
            if i != active_idx and not pkmn.is_fainted():
                actions.append(('switch', i))
                
        return actions

    def calculate_damage(self, attacker, defender, move):
        base_power = move["power"]
        # Dividimos la potencia de ataque entre 2.5 para que los combates duren más turnos
        # y la estrategia (ventaja de tipos, minimax) realmente importe.
        damage = ((attacker.attack / defender.defense) * (base_power / 2.5)) - (defender.speed * self.k)
        return max(1, int(damage))

    def check_win_condition(self):
        team1_fainted = all(p.is_fainted() for p in self.team1)
        team2_fainted = all(p.is_fainted() for p in self.team2)
        
        if team1_fainted: return 2
        if team2_fainted: return 1
        return 0

    def execute_turn(self, action_p1, action_p2):
        """Ejecuta el turno respetando la prioridad: Los cambios ocurren antes que los ataques."""
        
        # FASE 1: Resolución de Cambios (Switches)
        if action_p1[0] == 'switch':
            self.active_idx_1 = action_p1[1]
        if action_p2[0] == 'switch':
            self.active_idx_2 = action_p2[1]

        # FASE 2: Resolución de Ataques
        pkmn1 = self.get_active_pokemon(1)
        pkmn2 = self.get_active_pokemon(2)

        is_atk_p1 = action_p1[0] == 'attack'
        is_atk_p2 = action_p2[0] == 'attack'

        # Ambos atacan: decide la velocidad
        if is_atk_p1 and is_atk_p2:
            if pkmn1.speed >= pkmn2.speed:
                self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
                if not pkmn2.is_fainted():
                    self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])
            else:
                self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])
                if not pkmn1.is_fainted():
                    self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
                    
        # Solo P1 ataca (porque P2 cambió)
        elif is_atk_p1 and not pkmn1.is_fainted():
            self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
            
        # Solo P2 ataca (porque P1 cambió)
        elif is_atk_p2 and not pkmn2.is_fainted():
            self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])

    def _resolve_attack(self, attacker_id, attacker, defender, move_idx):
        """Función auxiliar para aplicar el daño."""
        move = attacker.moves[move_idx]
        dmg = self.calculate_damage(attacker, defender, move)
        defender.take_damage(dmg)