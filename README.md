# Pokefisi 🥊
**Simulación Estratégica de Combates Pokémon con Inteligencia Artificial**

Simulador avanzado de combates 3 vs 3 basado en mecánicas de Pokémon, desarrollado para explorar diferentes estrategias de IA. El proyecto implementa múltiples agentes cognitivos progresivamente más complejos, desde toma de decisiones aleatoria hasta un algoritmo Minimax optimizado mediante Algoritmos Genéticos.

## 📋 Tabla de Contenidos
- [Características](#características)
- [Arquitectura de Agentes](#-arquitectura-de-agentes)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-cómo-usar-el-proyecto)
- [Descripción de Módulos](#-módulos-principales)
- [Datos y Configuración](#-datos-y-configuración)
- [Resultados y Análisis](#-resultados-y-análisis)

## ✨ Características
- **Simulación realista:** Mecánicas basadas en Pokémon Showdown
- **Múltiples agentes IA:** Desde aleatorios hasta Minimax con poda alfa-beta
- **Interfaz gráfica:** Juega directamente contra la IA
- **Optimización genética:** Entrena y mejora agentes automáticamente
- **Batería de experimentos:** Ejecuta múltiples simulaciones y analiza resultados
- **Base de datos extensa:** Pokémon de múltiples generaciones (Gen 1-9) y modificaciones

## 🧠 Arquitectura de Agentes

El proyecto implementa una jerarquía de 4 niveles de agentes:

1. **Agente Aleatorio (Nivel 1)**
   - Toma decisiones completamente al azar
   - Sirve como base de referencia

2. **Agente Heurístico Básico - Greedy (Nivel 2)**
   - Usa heurísticas simples para evaluar movimientos
   - Selecciona el mejor movimiento disponible

3. **Agente Heurístico Avanzado (Nivel 3)**
   - Evalúa múltiples factores: HP, Velocidad, Ventaja de Tipos, Pokémon Vivos
   - Toma decisiones más estratégicas

4. **Agente Minimax con Poda Alfa-Beta (Nivel 4)**
   - Búsqueda en árbol de profundidad 3
   - Poda alfa-beta para optimización
   - Capacidad de cambiar Pokémon estratégicamente
   - Optimizado mediante Algoritmos Genéticos

## 📁 Estructura del Proyecto

```
PokeProyecto/
├── 📄 main.py                    # Punto de entrada principal
├── 🤖 agents.py                  # Definición de todos los agentes IA
├── 🌍 environment.py             # Simulador del combate y mecánicas del juego
├── 📊 data_loader.py             # Carga y procesa datos de Pokémon
├── 🧬 algoritmos_geneticos.py    # Algoritmo genético para optimizar agentes
├── 🧪 experimentos.py            # Batería de experimentos y análisis
├── 🎮 gui.py                     # Interfaz gráfica (Juega contra la IA)
├── 📈 resultados_experimentos.csv # Resultados de simulaciones
├── 📚 data/                      # Base de datos de Pokémon y mecánicas
│   ├── abilities.ts              # Habilidades de Pokémon
│   ├── items.ts                  # Objetos del juego
│   ├── moves.ts                  # Movimientos disponibles
│   ├── pokedex.ts                # Información de todas las especies
│   ├── pokemon_roster.json       # Lista de Pokémon
│   ├── typechart.ts              # Tabla de tipos y efectividad
│   ├── learnsets.ts              # Qué movimientos aprenden los Pokémon
│   ├── natures.ts                # Naturalezas y modificadores de stats
│   ├── conditions.ts             # Condiciones de estado (paralisis, etc)
│   ├── formats-data.ts           # Configuración de formatos de batalla
│   ├── rulesets.ts               # Reglas de juego
│   ├── scripts.ts                # Scripts del juego
│   ├── aliases.ts                # Alias de nombres
│   ├── pokemongo.ts              # Datos de Pokémon GO (opcional)
│   ├── tags.ts                   # Etiquetas de clasificación
│   ├── 🎨 mods/                  # Variaciones y mods del juego
│   │   ├── gen1/ - gen9/         # Datos por generación (1-9)
│   │   ├── afd/, biomechmons/    # Mods personalizados
│   │   ├── champions/, chatbats/ # Formatos especiales
│   │   └── ... (múltiples mods)
│   ├── 🎲 random-battles/        # Datos para batallas aleatorias por formato
│   └── 📝 text/                  # Recursos de texto
├── 📖 README.md                  # Este archivo
└── .gitignore
```

## 🔧 Instalación

### Requisitos previos
- **Python 3.8+**
- **pip** (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el repositorio:**
   ```bash
   cd PokeProyecto
   ```

2. **Instalar dependencias:**
   ```bash
   pip install requests
   ```
   - `requests`: Utilizado por `data_loader.py` para descargar datos de Pokémon Showdown

3. **Generar/actualizar la base de datos (opcional):**
   ```bash
   python data_loader.py
   ```
   Esto descarga y procesa la información más reciente de Pokémon si la carpeta `data/` no existe.

## 🚀 Cómo Usar el Proyecto

### 1. Jugar contra la IA (Interfaz Gráfica)
Interfaz interactiva donde puedes enfrentarte al agente Minimax:
```bash
python gui.py
```
- **Requisitos:** Asegurate que la base de datos `data/` existe
- **Cómo jugar:** Selecciona tus movimientos y cambia de Pokémon estratégicamente

### 2. Entrenar la IA (Algoritmo Genético)
Optimiza los parámetros del agente Minimax mediante Algoritmos Genéticos:
```bash
python algoritmos_geneticos.py
```
- Evolucionan parámetros de heurísticas
- Genera mejores agentes automáticamente
- Los resultados se guardan para posterior análisis

### 3. Ejecutar Batería de Experimentos
Realiza múltiples simulaciones y análisis comparativos:
```bash
python experimentos.py
```
- Compara el desempeño de diferentes agentes
- Ejecuta torneos entre agentes
- Genera estadísticas y métricas en `resultados_experimentos.csv`

### 4. Ejecutar el Programa Principal
Punto de entrada con opciones generales:
```bash
python main.py
```

## 📚 Módulos Principales

### `agents.py`
Define la lógica de todos los agentes IA:
- **RandomAgent:** Selecciona movimientos aleatoriamente
- **GreedyAgent:** Heurística simple de maximización
- **AdvancedAgent:** Heurística compleja con múltiples factores
- **MinimaxAgent:** Búsqueda Minimax con poda alfa-beta

### `environment.py`
Simula el ambiente del combate:
- Mecánicas de batalla (HP, velocidad, efectividad de tipos)
- Validación de acciones legales
- Manejo de cambios de Pokémon
- Cálculo de daño y estados

### `data_loader.py`
Gestiona la carga de datos:
- Descarga datos de Pokémon Showdown si es necesario
- Procesa archivos TypeScript en formatos utilizables
- Valida integridad de datos
- Cachea información para rápido acceso

### `algoritmos_geneticos.py`
Implementa optimización mediante Algoritmos Genéticos:
- Evoluciona parámetros de agentes
- Selección, cruzamiento y mutación
- Evaluación de aptitud mediante simulación
- Tracking de generaciones y mejoras

### `experimentos.py`
Coordina batería de experimentos:
- Define escenarios de prueba
- Ejecuta múltiples simulaciones
- Recopila estadísticas
- Exporta resultados a CSV

### `gui.py`
Interfaz gráfica para jugar:
- Visualización del estado de batalla
- Interfaz para seleccionar acciones
- Visualización del Pokémon enemigo
- Sistema de turnos interactivo

## 📊 Datos y Configuración

### Fuentes de Datos
- Todos los datos base provienen de **Pokémon Showdown**
- Incluye Pokémon de generaciones 1-9
- Múltiples formatos de batalla (competitive, casual, etc)

### Estructura de Datos
- **Pokédex (`pokedex.ts`):** Estadísticas, tipos, habilidades
- **Movimientos (`moves.ts`):** Potencia, precisión, efectos secundarios
- **Items (`items.ts`):** Bonificaciones, efectos en batalla
- **Tipos (`typechart.ts`):** Efectividad (super-efectivo, débil, resistente)
- **Naturalezas (`natures.ts`):** Modificadores de estadísticas

### Mods y Variaciones
- **Generaciones específicas:** Datos limitados a cada generación (Gen1-Gen9)
- **Modificaciones personalizadas:** Mods alternativos para experimentación
- **Batallas aleatorias:** Datos para generar equipos automáticos

## 📈 Resultados y Análisis

### Archivo de Resultados
Los resultados experimentales se guardan en **`resultados_experimentos.csv`** con:
- Comparativa de desempeño entre agentes
- Tasa de victorias/derrotas
- Estadísticas por formato de batalla
- Evolución del entrenamiento genético

### Cómo Analizar Resultados
```bash
# Abre el CSV con tu herramienta preferida
python -m pandas resultados_experimentos.csv  # O Excel, LibreOffice, etc
```

## 🎯 Casos de Uso

- **Investigación académica:** Análisis de estrategias de IA en juegos
- **Aprendizaje:** Entender algoritmos de búsqueda (Minimax, Alfa-Beta)
- **Optimización:** Mejorar agentes con Algoritmos Genéticos
- **Competición:** Torneo entre diferentes agentes
- **Diversión:** ¡Juega contra una IA fuerte!

## 📝 Notas de Desarrollo

- El proyecto está optimizado para simulaciones rápidas
- Los datos se cachean para mejorar performance
- La profundidad de búsqueda del Minimax puede ajustarse
- Soporta múltiples formatos de batalla simultáneamente

## 🤝 Contribuciones

Este es un proyecto educativo. Las mejoras y sugerencias son bienvenidas.