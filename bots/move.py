"""
The 'Move' class represents different actions that can be performed in a game. It contains static methods for waiting, spawning units, and building structures.

Attributes:
    _WAIT (str): Represents the action of waiting.
    _SPAWN (str): Represents the action of spawning units.
    _TURRET (str): Represents the action of building a turret.
    _FARM (str): Represents the action of building a farm.
"""

class Move:
    _WAIT = "W"
    _SPAWN = "S"
    _TURRET = "T"
    _FARM = "F"

    @classmethod
    def Wait(cls):
        """Returns the string representation of the wait action."""
        return Move._WAIT

    @classmethod
    def Spawn(cls, unit_type: str ):
        """Returns the string representation of the spawn action with the specified unit type."""
        return f"{Move._SPAWN} {unit_type.lower()}"

    class Build:
        @classmethod
        def Turret(cls, x: int = 0, y: int = 0):
            """Returns the string representation of building a turret at the specified coordinates."""
            return f"{Move._TURRET} {x} {y}"

        @classmethod
        def Farm(cls, x: int = 0, y: int = 0):
             """Returns the string representation of building a farm at the specified coordinates."""
            return f"{Move._FARM} {x} {y}"
