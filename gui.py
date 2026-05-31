import tkinter as tk
from tkinter import messagebox
import json
import random
from environment import Pokemon, Environment
from agents import MinimaxAgent, TYPE_MULTIPLIERS

# Paleta de colores Game Boy Original
GB_BG = "#9bbc0f"       # Verde claro (Fondo)
GB_DARK = "#0f380f"     # Verde oscuro (Texto y bordes)
GB_MID = "#306230"      # Verde medio
FONT_RETRO = ("Courier", 12, "bold")
FONT_TITLE = ("Courier", 16, "bold")

class PokefisiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("POKEFISI - Edición Game Boy")
        self.root.geometry("500x650")
        self.root.configure(bg=GB_BG)
        self.root.resizable(False, False)

        # Cargar Datos y Entorno
        self.init_game_state()

        # Construir Interfaz
        self.create_widgets()
        self.update_ui()
        self.log("¡Un Minimax salvaje ha aparecido!")
        self.log(f"¡Ve, {self.p1_active.name}!")

    def init_game_state(self):
        """Inicializa los equipos y la Inteligencia Artificial"""
        try:
            with open('data/pokemon_roster.json', 'r', encoding='utf-8') as f:
                roster = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Falta el archivo pokemon_roster.json")
            self.root.destroy()
            return
            
        team_names = random.sample(list(roster.keys()), 6)
        team1 = [Pokemon({**roster[n], 'name': n}) for n in team_names[:3]]
        team2 = [Pokemon({**roster[n], 'name': n}) for n in team_names[3:]]
        
        self.env = Environment(team1, team2)
        
        # Insertamos tu IA definitiva aquí (Ajusta los pesos si lo deseas)
        pesos = {'damage_score': 0.35, 'speed_score': 0.15, 'type_score': 0.25, 'alive_score': 0.25}
        self.ia_agent = MinimaxAgent(player_id=2, depth=3, weights=pesos)

    def create_widgets(self):
        # 1. PANTALLA DE COMBATE (Arriba)
        self.screen_frame = tk.Frame(self.root, bg=GB_BG, bd=4, relief=tk.SOLID, highlightbackground=GB_DARK)
        self.screen_frame.pack(pady=20, padx=20, fill=tk.X)

        # -- Oponente (Arriba Derecha) --
        self.opp_frame = tk.Frame(self.screen_frame, bg=GB_BG)
        self.opp_frame.pack(anchor="e", pady=10, padx=10)
        self.lbl_opp_name = tk.Label(self.opp_frame, text="RIVAL", font=FONT_TITLE, bg=GB_BG, fg=GB_DARK)
        self.lbl_opp_name.pack(anchor="e")
        self.lbl_opp_hp = tk.Label(self.opp_frame, text="HP: [||||||||||]", font=FONT_RETRO, bg=GB_BG, fg=GB_DARK)
        self.lbl_opp_hp.pack(anchor="e")

        # -- Jugador (Abajo Izquierda) --
        self.plyr_frame = tk.Frame(self.screen_frame, bg=GB_BG)
        self.plyr_frame.pack(anchor="w", pady=10, padx=10)
        self.lbl_plyr_name = tk.Label(self.plyr_frame, text="TÚ", font=FONT_TITLE, bg=GB_BG, fg=GB_DARK)
        self.lbl_plyr_name.pack(anchor="w")
        self.lbl_plyr_hp = tk.Label(self.plyr_frame, text="HP: [||||||||||]", font=FONT_RETRO, bg=GB_BG, fg=GB_DARK)
        self.lbl_plyr_hp.pack(anchor="w")

        # 2. CAJA DE TEXTO RETRO (Medio)
        self.log_frame = tk.Frame(self.root, bg=GB_DARK, bd=4)
        self.log_frame.pack(padx=20, fill=tk.X)
        self.text_box = tk.Text(self.log_frame, height=6, bg=GB_BG, fg=GB_DARK, font=("Courier", 10, "bold"), wrap=tk.WORD)
        self.text_box.pack(padx=2, pady=2, fill=tk.BOTH)
        self.text_box.config(state=tk.DISABLED)

        # 3. PANEL DE CONTROL / BOTONES (Abajo)
        self.controls_frame = tk.Frame(self.root, bg=GB_BG)
        self.controls_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.btn_moves = []
        for i in range(4):
            btn = tk.Button(self.controls_frame, text=f"Ataque {i}", font=FONT_RETRO, bg=GB_MID, fg=GB_BG, 
                            activebackground=GB_DARK, activeforeground=GB_BG,
                            command=lambda idx=i: self.process_turn(('attack', idx)))
            btn.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
            self.btn_moves.append(btn)
            
        self.btn_switch = tk.Button(self.controls_frame, text="🔄 RELEVAR", font=FONT_RETRO, bg=GB_DARK, fg=GB_BG,
                                    command=self.open_switch_menu)
        self.btn_switch.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

        for i in range(3):
            self.controls_frame.rowconfigure(i, weight=1)
        for i in range(2):
            self.controls_frame.columnconfigure(i, weight=1)

    def log(self, message):
        """Imprime texto en la caja de diálogo de la Game Boy"""
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"▶ {message}\n")
        self.text_box.see(tk.END)
        self.text_box.config(state=tk.DISABLED)

    def update_ui(self):
        """Actualiza nombres, barras de vida y textos de botones"""
        self.p1_active = self.env.get_active_pokemon(1)
        self.p2_active = self.env.get_active_pokemon(2)

        # Actualizar Etiquetas
        self.lbl_plyr_name.config(text=f"{self.p1_active.name.upper()} L50")
        self.lbl_opp_name.config(text=f"{self.p2_active.name.upper()} L50")
        
        # Barras de HP visuales (evita negativos si baja de 0)
        hp1_bars = max(0, int((self.p1_active.current_hp / self.p1_active.max_hp) * 10))
        hp2_bars = max(0, int((self.p2_active.current_hp / self.p2_active.max_hp) * 10))
        self.lbl_plyr_hp.config(text=f"HP: [{'█'*hp1_bars}{'-'*(10-hp1_bars)}] {self.p1_active.current_hp}")
        self.lbl_opp_hp.config(text=f"HP: [{'█'*hp2_bars}{'-'*(10-hp2_bars)}] {self.p2_active.current_hp}")

        # Actualizar Botones de Ataque
        if not self.p1_active.is_fainted():
            for i in range(4):
                move = self.p1_active.moves[i]
                self.btn_moves[i].config(text=f"{move['name']}\n({move['type']})", state=tk.NORMAL)
            self.btn_switch.config(state=tk.NORMAL)
        else:
            # ¡LA CORRECCIÓN! 
            # Si se debilita, apagamos los ataques pero ENCENDEMOS el relevo
            for btn in self.btn_moves: 
                btn.config(state=tk.DISABLED)
            self.btn_switch.config(state=tk.NORMAL) 
            
            self.log(f"¡{self.p1_active.name} se desmayó! Selecciona RELEVAR.")
            
    def open_switch_menu(self):
        """Abre una ventana emergente para elegir otro Pokémon"""
        switch_win = tk.Toplevel(self.root)
        switch_win.title("Seleccionar Pokémon")
        switch_win.geometry("300x250")
        switch_win.configure(bg=GB_BG)
        
        tk.Label(switch_win, text="Elige tu relevo:", font=FONT_TITLE, bg=GB_BG, fg=GB_DARK).pack(pady=10)
        
        for i, pkmn in enumerate(self.env.team1):
            state = tk.NORMAL if not pkmn.is_fainted() and i != self.env.active_idx_1 else tk.DISABLED
            text = f"{pkmn.name} (HP: {pkmn.current_hp})"
            btn = tk.Button(switch_win, text=text, font=FONT_RETRO, bg=GB_MID, fg=GB_BG, state=state,
                            command=lambda idx=i, w=switch_win: [w.destroy(), self.process_turn(('switch', idx))])
            btn.pack(pady=5, fill=tk.X, padx=20)

    def process_turn(self, player_action):
        """Ejecuta el turno completo después de que el usuario hace clic"""
        # Desactivar botones temporalmente para evitar spam de clics
        for btn in self.btn_moves: btn.config(state=tk.DISABLED)
        self.btn_switch.config(state=tk.DISABLED)
        
        self.log("-" * 20)
        
        # 1. Obtener acción de la IA
        self.log("La IA está pensando...")
        self.root.update() # Fuerza a la interfaz a mostrar el texto antes del lag del Minimax
        
        ai_action = self.ia_agent.choose_action(self.env)
        
        # 2. Registrar cambios antes del turno para la narrativa
        if player_action[0] == 'switch':
            self.log(f"¡Vuelve! ¡Ve {self.env.team1[player_action[1]].name}!")
        if ai_action[0] == 'switch':
            self.log(f"El Rival envió a {self.env.team2[ai_action[1]].name}!")

        # 3. Ejecutar Matemáticas en el Entorno
        hp_p1_before = self.p1_active.current_hp
        hp_p2_before = self.p2_active.current_hp
        
        self.env.execute_turn(player_action, ai_action)
        self.update_ui()
        
        # 4. Narrar los ataques
        p1_new = self.env.get_active_pokemon(1)
        p2_new = self.env.get_active_pokemon(2)
        
        if player_action[0] == 'attack' and not self.p1_active.is_fainted():
            dmg = hp_p2_before - p2_new.current_hp
            if dmg > 0: self.log(f"Tu {self.p1_active.name} hizo {dmg} pts de daño.")
                
        if ai_action[0] == 'attack' and not self.p2_active.is_fainted():
            dmg = hp_p1_before - p1_new.current_hp
            if dmg > 0: self.log(f"El Rival atacó e hizo {dmg} pts de daño.")

        # 5. Revisar si alguien ganó
        win = self.env.check_win_condition()
        if win == 1:
            self.log("¡HAS DERROTADO A LA IA MINIMAX!")
            messagebox.showinfo("¡VICTORIA!", "¡Has derrotado al Algoritmo Minimax!")
            self.root.destroy()
        elif win == 2:
            self.log("La IA te ha aplastado...")
            messagebox.showinfo("DERROTA", "El Algoritmo Minimax ha ganado la partida.")
            self.root.destroy()
        else:
            # Si el juego sigue, reactivamos la interfaz (update_ui lo hace automáticamente si el PKMN sigue vivo)
            self.update_ui()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = PokefisiGUI(ventana)
    ventana.mainloop()