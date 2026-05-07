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
        """
        Inicializa el entorno de combate.
        team1 y team2 deben ser listas de objetos Pokemon (ej. 3 vs 3 o 4 vs 4).
        """
        self.team1 = team1
        self.team2 = team2
        self.k = k_factor # Factor de ajuste para la fórmula
        
        # Índices del Pokémon activo en el campo
        self.active_idx_1 = 0
        self.active_idx_2 = 0

    def get_active_pokemon(self, player):
        """Devuelve el Pokémon que está peleando actualmente."""
        if player == 1:
            return self.team1[self.active_idx_1]
        return self.team2[self.active_idx_2]

    def calculate_damage(self, attacker, defender, move):
        """
        Aplica estrictamente la fórmula de la rúbrica:
        Damage = (Attack / Defense_op) * BasePower - Speed_op * K
        """
        base_power = move["power"]
        
        # Fórmula requerida por el profesor
        damage = (attacker.attack / defender.defense) * base_power - (defender.speed * self.k)
        
        # El daño no puede ser negativo ni menor a 1 si el ataque acierta
        return max(1, int(damage))

    def check_win_condition(self):
        """El combate termina cuando todos los Pokémon de un jugador tienen HP = 0"""
        team1_fainted = all(p.is_fainted() for p in self.team1)
        team2_fainted = all(p.is_fainted() for p in self.team2)
        
        if team1_fainted:
            return 2 # Gana jugador 2
        elif team2_fainted:
            return 1 # Gana jugador 1
        return 0 # El combate continúa

    def execute_turn(self, action_p1, action_p2):
        """
        Ejecuta un turno básico. 
        Por ahora, action_p1 y action_p2 son los índices de los movimientos elegidos.
        """
        pkmn1 = self.get_active_pokemon(1)
        pkmn2 = self.get_active_pokemon(2)
        
        move1 = pkmn1.moves[action_p1]
        move2 = pkmn2.moves[action_p2]

        # Determinar quién ataca primero por velocidad
        if pkmn1.speed >= pkmn2.speed:
            first, second = pkmn1, pkmn2
            move_first, move_second = move1, move2
        else:
            first, second = pkmn2, pkmn1
            move_first, move_second = move2, move1

        # Turno del más rápido
        dmg_first = self.calculate_damage(first, second, move_first)
        second.take_damage(dmg_first)

        # Turno del más lento (solo ataca si no fue debilitado)
        if not second.is_fainted():
            dmg_second = self.calculate_damage(second, first, move_second)
            first.take_damage(dmg_second)