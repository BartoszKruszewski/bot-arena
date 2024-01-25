# Python Bot Package
The purpose of this package is to facilitate the design of bots for Bot-Arena. The `Bot` class serves as a template for creating subsequent bots, allowing customization of their behavior for different game strategies.

## Bot Class

The `Bot` class is a template for implementing bots in your program.

### Attributes:
- `game_timeout (int)`: Time available to make a move in the game.
- `move_timeout (int)`: Time available for movement in the game.
- `ready_timeout (int)`: Waiting time for readiness.
- `side (str)`: The side to which the bot is assigned.
- `status (str)`: Current game status.
- `arena_properties (str)`: Game arena properties.
---
### Methods:
- `preprocess(self) -> None`: Prepares the robot for the start of the game.
- `make_move(self) -> str`: Invokes the robot's logic to create a move.
- `post_move_action(self) -> None`: Performs additional actions after a move in the game loop.
- `run(self) -> None`: Runs the main robot loop.
---
### Example Usage:
```python
class MyBot(Bot):
    def preprocess(self):
        # Your custom logic before the start of the game

    def make_move(self):
        # Your custom logic for generating a move
        return Move.Wait()  # Default action is waiting; replace it with your logic

    def post_move_action(self):
        # Your custom logic after a move

if __name__ == "__main__":
    my_bot = MyBot()
    my_bot.run()
```

**Note:**

- Override provided methods to customize the bot's behavior.
- The `receive_game_properties` and `receive_arena_properties` methods are used for receiving external input.
- Adjust the input format according to the example for `arena_properties`.
- The `Move` class is used to generate moves in the `make_move` method.
- Customize and expand the template to implement unique bot strategies according to your needs.
---
**Input Format: JSON for Arena Properties:**

Values for `arena_properties` are expected in JSON format, as shown below:

```python
{
    'arena': {
        'base': {
            'left': [x_left, y_left],  # Coordinates of the base on the left side
            'right': [x_right, y_right]  # Coordinates of the base on the right side
        },
        'path': [
            [x1, y1],  # Coordinates of a point on the path
            [x2, y2],
            # ...
        ],
        'obstacles': [
            [ox1, oy1],  # Coordinates of an obstacle
            [ox2, oy2],
            # ...
        ],
        'map_size': [width, height]  # Map size
    },
    'players': {
        'left': {
            'buildings': {
                'turrets': [
                    [tx1, ty1],  # Coordinates of a turret
                    [tx2, ty2],
                    # ...
                ],
                'farms': [
                    [fx1, fy1],  # Coordinates of a farm
                    [fx2, fy2],
                    # ...
                ]
            },
            'units': [
                [ux1, uy1],  # Unit position
                [ux2, uy2],
                # ...
            ],
            'gold': left_player_gold,  # Gold amount for the player on the left side
            'income': left_player_income  # Income for the player on the left side
        },
        'right': {
            'buildings': {
                'turrets': [
                    # ...
                ],
                'farms': [
                    # ...
                ]
            },
            'units': [
                # ...
            ],
            'gold': right_player_gold,  # Gold amount for the player on the right side
            'income': right_player_income  # Income for the player on the right side
        }
    }
}
```

## Move Class

The `Move` class represents various actions that can be taken in the game. It includes static methods for waiting, unit creation, and structure building.

### Methods:
- `Wait(cls)`: Returns a string representing a waiting action.
- `Spawn(cls, unit_type: str)`: Returns a string representing a unit creation action with the specified type.

#### Build:
- `Build.Turret(cls, x: int = 0, y: int = 0)`: Returns a string representing turret construction at specified coordinates.
- `Build.Farm(cls, x: int = 0, y: int = 0)`: Returns a string representing farm construction at specified coordinates.
---
### Example Usage:
```python
move_spawn = Move.Spawn("Archer")  # Represents spawning an "Archer" unit
move_turret = Move.Build.Turret(3, 5)  # Represents building a turret at coordinates (3, 5)
move_farm = Move.Build.Farm(2, 4)  # Represents building a farm at coordinates (
```
