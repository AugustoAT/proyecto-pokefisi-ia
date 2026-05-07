# PokeProyecto 🔴

Un simulador interactivo de combate Pokémon implementado en Python, donde puedes jugar contra diferentes agentes de IA con distintos niveles de inteligencia.

## 📋 Descripción

PokeProyecto es un proyecto educativo que implementa un sistema completo de combate Pokémon basado en:
- **Fórmula matemática realista**: Cálculo de daño basado en ataque, defensa, poder del movimiento y velocidad
- **Múltiples agentes de IA**: Desde comportamiento aleatorio hasta heurísticas inteligentes
- **Modo interactivo**: Juega directamente contra la CPU desde la consola
- **Base de datos real**: Utiliza datos de Pokémon Showdown (Generaciones 1-3)

## 🎮 Características Principales

- **Sistema de combate realista**: Implementación de la fórmula de daño: `Damage = (Attack / Defense) * BasePower - Speed * K`
- **Tres tipos de agentes**:
  - 🎲 **Agente Aleatorio**: Elige acciones sin criterio (baseline)
  - 🧠 **Agente Heurístico**: Maximiza daño basado en diferencia de HP
  - 👤 **Agente Humano**: Control total del jugador vía consola
- **Equipos balanceados**: 3 Pokémon por jugador, seleccionados aleatoriamente
- **Movimientos variados**: 4 movimientos elegidos aleatoriamente de 8 disponibles por Pokémon
- **Combate por turnos**: Orden determinado por velocidad (Stat SPE)

## 🏗️ Estructura del Proyecto

```
PokeProyecto/
├── main.py              # Punto de entrada - Lógica del combate interactivo
├── agents.py            # Implementación de los tres tipos de agentes
├── environment.py       # Clase Pokemon y Environment (motor de combate)
├── data_loader.py       # Generador de roster desde API de Pokémon Showdown
├── data/
│   └── pokemon_roster.json   # Base de datos procesada (30 Pokémon Gen 1-3)
└── README.md            # Este archivo
```

## 📦 Requisitos

- **Python 3.8+**
- **Librerías**:
  - `requests` - Para descargar datos de Pokémon Showdown

## ⚙️ Instalación

1. **Clonar o descargar el repositorio**:
```bash
cd PokeProyecto
```

2. **Instalar dependencias**:
```bash
pip install requests
```

3. **Generar la base de datos** (opcional - la primera vez):
```bash
python data_loader.py
```

## 🚀 Cómo Usar

### Jugar Contra la IA

```bash
python main.py
```

El programa:
1. Carga 2 equipos aleatorios de Pokémon
2. Te asigna el control (Jugador 1 - HumanAgent)
3. La CPU juega automáticamente (Jugador 2 - BasicHeuristicAgent)
4. Por cada turno, selecciona uno de los 4 movimientos disponibles
5. El combate continúa hasta que todos los Pokémon de un equipo sean debilitados

**Ejemplo de sesión**:
```
Cargando base de datos...

========================================
¡COMIENZA EL COMBATE POKEFISI INTERACTIVO!
========================================

--- Turno 1 ---
J1 (TÚ): Pikachu [HP: 45/45]
J2 (CPU): Charizard [HP: 78/78]

--- Tu Turno ---
¿Qué debería hacer Pikachu?
  [0]: Thunderbolt (Poder: 90, Tipo: Electric)
  [1]: Thunder Wave (Poder: 0, Tipo: Electric)
  [2]: Quick Attack (Poder: 40, Tipo: Normal)
  [3]: Iron Tail (Poder: 100, Tipo: Steel)

Elige el número de tu movimiento (0-3): 0

> Tu Pikachu usó su ataque e hizo 25 de daño.
> El Charizard enemigo atacó e hizo 18 de daño.
```

## 🤖 Agentes

### Agent (Clase Base)
Clase abstracta que define la interfaz común para todos los agentes.

```python
class Agent:
    def choose_action(self, environment):
        raise NotImplementedError
```

### RandomAgent - Agente Aleatorio (Nivel 1)
- **Comportamiento**: Selecciona uno de los 4 movimientos al azar
- **Uso**: Baseline para comparación
- **Complejidad**: O(1)

```python
jugador = RandomAgent(player_id=1)
```

### BasicHeuristicAgent - Agente Heurístico (Nivel 2)
- **Comportamiento**: Simula todos los ataques disponibles y elige el que máximo daño hace
- **Estrategia**: Maximizar la diferencia de HP a su favor
- **Complejidad**: O(n) donde n = número de movimientos (4)

```python
jugador = BasicHeuristicAgent(player_id=2)
```

### HumanAgent - Agente Humano
- **Comportamiento**: Espera entrada del usuario por consola
- **Validación**: Garantiza que el input sea válido (0-3)
- **Interfaz**: Muestra estadísticas de cada movimiento

```python
jugador = HumanAgent(player_id=1)
```

## 🎯 Clases Principales

### Pokemon
Representa un Pokémon individual con:
- **Atributos**: Nombre, tipos, estadísticas (HP, ATK, DEF, SPE)
- **Movimientos**: 4 elegidos aleatoriamente de 8 disponibles
- **Métodos**:
  - `is_fainted()`: Verifica si tiene 0 HP
  - `take_damage(damage)`: Aplica daño (mínimo 0 HP)

```python
pkmn = Pokemon(data_dict)
pkmn.take_damage(25)
```

### Environment
Motor de combate que gestiona:
- **Equipos**: Lista de Pokémon por jugador
- **Estado activo**: Índice del Pokémon en combate
- **Turno**: Cálculo de daño y orden de ataque

**Métodos principales**:
- `get_active_pokemon(player)`: Devuelve el Pokémon en combate
- `calculate_damage(attacker, defender, move)`: Calcula daño con la fórmula matemática
- `check_win_condition()`: Determina al ganador (0=continúa, 1=J1, 2=J2)
- `execute_turn(action_p1, action_p2)`: Ejecuta un turno completo

## 📊 Fórmula de Daño

La fórmula de cálculo de daño se basa en:

$$\text{Damage} = \max(1, \left\lfloor \frac{\text{ATK}}{\text{DEF}_{\text{opp}}} \times \text{BasePower} - \text{SPE}_{\text{opp}} \times K \right\rfloor)$$

Donde:
- **ATK**: Estadística de ataque del atacante
- **DEF_opp**: Estadística de defensa del defensor
- **BasePower**: Poder base del movimiento
- **SPE_opp**: Estadística de velocidad del defensor
- **K**: Factor de ajuste (por defecto 0.5)

## 📊 Flujo del Combate

```
1. Cargar equipos aleatorios
2. MIENTRAS no hay ganador:
   a. Mostrar estado de Pokémon activos
   b. Obtener acción del Jugador 1 (HumanAgent)
   c. Obtener acción del Jugador 2 (CPU)
   d. Ejecutar turno:
      - Determinar quién ataca primero (por SPE)
      - Calcular y aplicar daño
      - Verificar si alguien fue debilitado
   e. Si no hay ganador, continuar
3. Mostrar ganador
```

## 💾 Base de Datos

### Generación del Roster
El archivo `data_loader.py` descarga y procesa datos de Pokémon Showdown:

```bash
python data_loader.py
```

**Características**:
- 30 Pokémon de Generaciones 1-3 (aleatorios)
- 8 movimientos por Pokémon (con BasePower > 0)
- Estadísticas reales de Pokémon Showdown
- Formato JSON limpio y optimizado

**Estructura del JSON**:
```json
{
  "Pikachu": {
    "id": 25,
    "types": ["Electric"],
    "stats": {
      "hp": 35,
      "atk": 55,
      "def": 40,
      "spa": 50,
      "spd": 50,
      "spe": 90
    },
    "moves": [
      {
        "name": "Thunderbolt",
        "power": 90,
        "type": "Electric",
        "accuracy": 100
      }
    ]
  }
}
```

## 🔧 Personalización

### Cambiar Jugadores
En `main.py`, puedes cambiar los agentes:

```python
# Jugar como RandomAgent vs BasicHeuristicAgent
jugador1 = RandomAgent(player_id=1)
jugador2 = BasicHeuristicAgent(player_id=2)
run_battle(jugador1, jugador2, equipo1, equipo2)
```

### Ajustar Parámetros
En `environment.py`:
```python
# Factor de ajuste de la fórmula de daño
env = Environment(team1, team2, k_factor=0.5)

# Número de Pokémon por equipo
equipo1 = load_team('data/pokemon_roster.json', num_pokemon=4)
```

En `data_loader.py`:
```python
MAX_DEX_NUM = 386   # Cambiar generación máxima
ROSTER_SIZE = 50    # Cambiar cantidad de Pokémon
MOVES_PER_PKMN = 12 # Cambiar movimientos disponibles
```

## 📝 Notas Técnicas

- **Velocidad en turnos**: El Pokémon con mayor SPE ataca primero
- **Daño mínimo**: El daño mínimo posible es 1 (nunca 0)
- **Derrota**: Un Pokémon es debilitado cuando HP ≤ 0
- **Cambio de Pokémon**: Automático cuando el activo es debilitado
- **Final del combate**: Cuando todos los Pokémon de un equipo están debilitados

## 🎓 Objetivos de Aprendizaje

Este proyecto demuestra:
- ✅ Programación orientada a objetos en Python
- ✅ Patrones de diseño (Strategy con agentes)
- ✅ Integración con APIs externas (Pokémon Showdown)
- ✅ Simulación y sistemas de turnos
- ✅ Aplicación de fórmulas matemáticas en videojuegos
- ✅ Entrada/salida por consola interactiva

## 🚀 Futuras Mejoras

- [ ] Interfaz gráfica (Tkinter/Pygame)
- [ ] Más tipos de agentes (Redes neuronales, Minimax, Alpha-Beta pruning)
- [ ] Sistema de tipos de Pokémon (efectividad)
- [ ] Efectos de estado (paralizado, quemado, etc.)
- [ ] Habilidades de Pokémon
- [ ] Estrategias de cambio de Pokémon
- [ ] Sistema de torneos

## 📄 Licencia

Este proyecto es educativo y usa datos de Pokémon Showdown bajo su respectiva licencia.

---

**Autor**: Augusto, Fernando, Frank  
**Fecha de creación**: 2025  
**Versión**: 1.0
