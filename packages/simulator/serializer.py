from ..game_logic.objects.map import Map

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

    def serialize_arena(game: Game) -> dict:
        # Arena data
        path = game.get_path();
        start = path[0]
        end = path[-1]

        obstacles = game.get_obstacles()
        return {
            'start': start,
            'end': end,
            'path': path,
            'obstacles': obstacles,
        }

    def serialize_player(game: Game, player_side: str) -> dict:
        player_data = {
            'structures': game.get_structures()[player_side],
            'stats': game.get_stats()[player_side]
        }
        return player_data