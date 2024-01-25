import json

from packages.game_logic.game import Game

class Serializer:
    @staticmethod
    def get_json(game: Game):
        serialized_data = Serializer.serialize(game)
        json_string = json.dumps(serialized_data)
        return json_string

    @staticmethod
    def serialize(game: Game):
        game_data = {
            'arena': Serializer.serialize_arena(game),
            'players': {
                'left': Serializer.serialize_player(game, 'left'),
                'right': Serializer.serialize_player(game, 'right')
            }
        }
        return game_data

    @staticmethod
    def serialize_arena(game: Game) -> dict:
        # Arena data
        path = game.get_path()
        base_left = path[0]
        base_right = path[-1]

        map_size = game.get_map_size()
        obstacles = [obstacle.cords for obstacle in game.get_obstacles()]

        return {
            'base': {
                'left': base_left,
                'right': base_right
            },
            'path': path,
            'obstacles': obstacles,
            'map_size': map_size
        }


    @staticmethod
    def serialize_player(game: Game, player_side: str) -> dict:
        turrets_data = game.get_turrets()[player_side]
        farms_data = game.get_farms()[player_side]
        units_data = game.get_soldiers()[player_side]

        turrets_serialized = [turret.get_coordinates() for turret in turrets_data]
        farms_serialized = [farm.get_coordinates() for farm in farms_data]
        units_serialized = [unit.get_position() for unit in units_data]

        player_data = {
            'buildings': {
                'turrets': turrets_serialized,
                'farms': farms_serialized
            },
            'units': units_serialized,
            'gold': game.get_gold()[player_side],
            'income': game.get_income()[player_side]
        }
        return player_data


if __name__ == '__main__':
    game = Game()

    serialized_game = Serializer.get_json(game)
    print(serialized_game)
