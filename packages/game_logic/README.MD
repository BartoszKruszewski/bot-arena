# Game Logic

## Description

`game_logic` package is responsible for the game state, game rules and possible moves.

## Contents

### Actions

```python
from game_logic.actions import Wait, SpawnSoldier, BuildTurret
```

Each action takes a `side` argument and optionally other arguments.
`side` can be either `"left"` or `"right"`.

```python
Wait("left")
SpawnSoldier("left")
# BuildTurres takes 3 arguments: side, x, y
BuildTurret("right", 1, 2)
```

### Game

```python
from game_logic import Game
```

Game class is responsible for the game state and rules.

Public methods:

```python
# Main method, returns tuple of ErrorCode
Game.update(action_left: Action, action_right: Action) -> tuple[str, str]

# Map methods
Game.get_path() -> list[tuple[int, int]]
Game.get_obstacles() -> list[tuple[int, int]]
Game.get_map_size() -> tuple[int, int] # (width, height)

# Below methods return a dictionary with keys "left" and "right"
Game.get_turrets() -> dict[str, list[Turret]]
Game.get_soldiers() -> dict[str, list[Soldier]]
Game.get_stats() -> dict[str, int]
```

#### ErrorCode

```python
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

Soldier class represents a soldier on the map.
Public attributes:

```python
Soldier.id: int
Soldier.hp: int
Soldier.dmg: int

# Position on path, use Game.get_path()[position] to get the coordinates
Soldier.position: int
```

#### Turret

Turret class represents a turret on the map.
Public attributes:

```python
Turret.cords: tuple[int, int] # (x, y)
Turret.attack: int
Turret.id: int
Turret.range: int
```

## Usage

```python
from game_logic import Game
from game_logic import Wait, SpawnSoldier, BuildTurret

action_left = Wait("left")
action_right = SpawnSoldier("right")

game = Game()
game_response = game.update(action_left, action_right)
print(game_response)
```

> `('OK', 'OK')`
