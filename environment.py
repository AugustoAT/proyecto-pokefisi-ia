import random

# Las leyes físicas de los tipos ahora viven en el Environment
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

class Pokemon:
    def __init__(self, data_dict):
        self.name = data_dict["name"] 
        self.types = data_dict["types"]
        self.max_hp = data_dict["stats"]["hp"]
        self.current_hp = self.max_hp
        self.attack = data_dict["stats"]["atk"]
        self.defense = data_dict["stats"]["def"]
        self.speed = data_dict["stats"]["spe"]
        self.moves = data_dict.get("moves", [])
        
    def is_fainted(self):
        return self.current_hp <= 0

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

class Environment:
    # Redujimos K a 0.2 para que la velocidad no te haga inmortal
    def __init__(self, team1, team2, k_factor=0.2):
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
        actions = []
        active_pkmn = self.get_active_pokemon(player_id)
        if not active_pkmn.is_fainted():
            for i in range(len(active_pkmn.moves)):
                actions.append(('attack', i))
        team = self.team1 if player_id == 1 else self.team2
        active_idx = self.active_idx_1 if player_id == 1 else self.active_idx_2
        for i, pkmn in enumerate(team):
            if i != active_idx and not pkmn.is_fainted():
                actions.append(('switch', i))
        return actions

    def calculate_damage(self, attacker, defender, move):
        base_power = move["power"]
        
        # 1. Fórmula base requerida por la rúbrica
        raw_damage = (attacker.attack / defender.defense) * base_power - (defender.speed * self.k)
        
        # Evitar daños negativos antes de aplicar tipos
        raw_damage = max(5, raw_damage) 

        # 2. Calcular Multiplicador de Tipos
        multiplier = 1.0
        for t in defender.types:
            multiplier *= TYPE_MULTIPLIERS.get(move["type"], {}).get(t, 1.0)
            
        # 3. Aplicar tipos y un divisor global para balancear la duración de la partida
        final_damage = (raw_damage * multiplier) / 2.0
        
        return max(1, int(final_damage))

    def check_win_condition(self):
        team1_fainted = all(p.is_fainted() for p in self.team1)
        team2_fainted = all(p.is_fainted() for p in self.team2)
        if team1_fainted: return 2
        if team2_fainted: return 1
        return 0

    def execute_turn(self, action_p1, action_p2):
        if action_p1[0] == 'switch': self.active_idx_1 = action_p1[1]
        if action_p2[0] == 'switch': self.active_idx_2 = action_p2[1]

        pkmn1 = self.get_active_pokemon(1)
        pkmn2 = self.get_active_pokemon(2)
        is_atk_p1 = action_p1[0] == 'attack'
        is_atk_p2 = action_p2[0] == 'attack'

        if is_atk_p1 and is_atk_p2:
            if pkmn1.speed >= pkmn2.speed:
                self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
                if not pkmn2.is_fainted():
                    self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])
            else:
                self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])
                if not pkmn1.is_fainted():
                    self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
        elif is_atk_p1 and not pkmn1.is_fainted():
            self._resolve_attack(1, pkmn1, pkmn2, action_p1[1])
        elif is_atk_p2 and not pkmn2.is_fainted():
            self._resolve_attack(2, pkmn2, pkmn1, action_p2[1])

    def _resolve_attack(self, attacker_id, attacker, defender, move_idx):
        move = attacker.moves[move_idx]
        dmg = self.calculate_damage(attacker, defender, move)
        defender.take_damage(dmg)