from ..game_logic.game import Game

class Serializer:
    def __init__(self):
        pass

    def get(game: Game) -> dict[dict[str, str], dict[dict[str, str], dict[str, str]]]:
        game_data = {
            'arena': Serializer.serialize_arena(game),
            'players' : {
                'leftPlayer': Serializer.serialize_player(game, 'left'),
                'rightPlayer': Serializer.serialize_player(game, 'right')
            }
        }

        return game_data

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
        turrets_data = game.get_turrets()[player_side]

        turrets_cords = []

        for turret in turrets_data:
            turrets_cords.append(turret.cords)

        player_data = {
            'turrets': turrets_cords,
            'gold': game.get_gold()[player_side]
        }
        return player_data


if __name__ == '__main__':
    game = Game()

    game = Serializer.get(game)
    print(game)

