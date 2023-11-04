import json

from packages.game_logic.game import Game
from packages.game_logic.actions import *
from packages.game_logic.objects.turrets import Turrets


class Serializer:
    def __init__(self):
        pass

    def get(game: Game) -> json:
        game_data = {
            'arena': Serializer.serialize_arena(game),
            'players' : {
                'leftPlayer': Serializer.serialize_player(game, 'left'),
                'rightPlayer': Serializer.serialize_player(game, 'right')
            }
        }

        gameJSON = json.dumps(game_data)

        return gameJSON

    def serialize_arena(game: Game) -> dict[str, str]:
        # Arena data
        path = game.get_path();
        start = path[0]
        end = path[-1]

        map_size = game.get_map_size()
        obstacles = game.get_obstacles()

        return {
            'start': start,
            'end': end,
            'path': path,
            'obstacles': obstacles,
            'map_size': map_size
        }

    def serialize_player(game: Game, player_side: str) -> dict[str, str]:
        # turrets_data = game.get_turrets()[player_side]
        #
        # turret_coords = {}
        # for i in turrets_data:
        #     turret_coords[i] = turrets_data.getcoords()

        player_data = {
            'turrets': game.get_turrets(),
            'stats': game.get_stats()[player_side]
        }
        return player_data

if __name__ == '__main__':
    game = Game()
    #
    # log = game.update(BuildTurret('left', (0, 1)),Wait('right'))
    # print(log)

    game = Serializer.get(game)
    print(game)