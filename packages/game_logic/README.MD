# Game Logic

`game_logic` package is responsible for the game state, game [rules](#rules) and possible moves.

## Contents

### Actions

```python
from game_logic.actions import Wait, SpawnSoldier, BuildTurret, BuildFarm
```

Each action takes a `side` argument and optionally other arguments.
`side` can be either `"left"` or `"right"`.

```python
Wait("left")
# list of soldier names can be found in game_logic.stats.py
SpawnSoldier("left", "soldier_name")
# Builds takes 3 arguments: side, x, y
BuildTurret("right", 1, 2)
BuildFarm("left", 3, 4)
```

### Game

```python
from game_logic import Game
```

Game class is responsible for the game state and [rules](#rules). Each call to `Game.update` updates the game state including:
- [Soldiers](#soldier)
- [Turrets](#turret) 
- [Farms](#farm)

and returns a tuple of two strings representing the game [result](#ErrorCode) for each side.

Public methods:

```python
Game.update(action_left: Action, action_right: Action) -> tuple[str, str]

# Map methods
Game.get_path() -> list[tuple[int, int]]
Game.get_obstacles() -> list[tuple[int, int]]
Game.get_map_size() -> tuple[int, int] # (width, height)

# Below methods return a dictionary with keys "left" and "right"
Game.get_soldiers() -> dict[str, list[Soldier]]
Game.get_turrets() -> dict[str, list[Turret]]
Game.get_farms() -> dict[str, list[Farm]]
Game.get_gold() -> dict[str, int]
Game.get_income() -> dict[str, int]
```

#### ErrorCode

```python
from game_logic import ErrorCode

ErrorCode = {
    -5: 'Too many troops',
    -4: 'Wrong build place',
    -3: 'Same build place',
    -2: 'Wrong action',
    -1: 'Not enough gold',
    0: 'OK',
    1: 'Left win',
    2: 'Right win',
    3: 'Tie'
}
```

#### Soldier

Public attributes:

```python
Soldier.id: int
Soldier.max_hp: int
Soldier.range: int

Soldier.hp: int
Soldier.damage: int
# Position on path, use Game.get_path()[position] to get the coordinates
Soldier.position: int
```

#### Turret

Public attributes:

```python
Turret.cords: tuple[int, int] # (x, y)
Turret.attack: int
Turret.id: int
Turret.range: int
```

#### Farm

Public attributes:

```python
Farm.cords: tuple[int, int] # (x, y)
Farm.id: int
```

## Usage

```python
from game_logic import Game
from game_logic import Wait, SpawnSoldier, BuildTurret
from game_logic import ErrorCode

action_left = Wait("left")
action_right = SpawnSoldier("right", "basic")

game = Game()
game_response = game.update(action_left, action_right)
print(game_response)
if (ErrorCode[0], ErrorCode[0]) == game_response print("Action Succesful")
# ('OK', 'OK')
```

## Rules
The game is turn-based. Each turn, each player can perform one action. The game ends when one of the players soldiers reaches the end of the path.

### Map
The map is a generated randomly grid where each cell can contain one of the following: empty, obstacle, farm, turret, soldier. 

### Actions
Each turn, each player can perform one of the following actions:
- Wait - do nothing
- Spawn soldier - spawn a soldier on the first cell of the path
- Build turret - build a turret on an empty cell
- Build farm - build a farm on an empty cell, farms generate additional income

### Turn
Turn consists of the following steps:
- Additional income is added to each player
- Turrets and soldiers are [choosing their targets](#targeting)
- Turrets and soldiers are attacking their targets
- Soldiers are moving forward if are not in combat
- Players actions are performed
- Players gold is updated based on their income

#### Targeting
Soldiers are choosing their targets based on their range. If there are multiple targets in range, the closest one is chosen. 

Turrets are choosing their targets based on their range. If there are multiple targets in range, the one closest to the end of the path is chosen.



