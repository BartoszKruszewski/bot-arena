import time
import sys

from .bot import Bot
from .serializer import Serializer
from .log_maker import LogMaker
from packages.game_logic.game import Game, ErrorCode
from packages.game_logic.actions import Wait, BuildFarm, BuildTurret, SpawnSoldier

class WrongMove(Exception):
    pass

def str_to_action(str, player):
    side = "left" if player == 0 else "right"
    str = str.split()
    if str[0] == "W":
        return Wait(side)
    elif str[0] == "T":
        return BuildTurret(side, str[1], str[2])
    elif str[0] == "F":
        return BuildFarm(side, str[1], str[2])
    elif str[0] == "S":
        return SpawnSoldier(side, str[1])
    else:
        raise WrongMove

def play(name1, name2, num_games,
        ready_timeout=10, move_timeout=10, game_timeout=60):
        
        p = {}

        def reset():
            if not p:
                for player in p.values():
                    player.kill()
                p[0] = Bot(name1)
                p[1] = Bot(name2)
           
            for player in p.values():
                player.put(f'SETTINGS {game_timeout} {move_timeout} {ready_timeout} {player}')
                player.total_time = 0.0

        results = []

        def determine(dict : dict[int, bool]):
            if not dict[p[0]] and not dict[p[1]]:
                return 'TIE'
            elif not dict[p[0]]:
                return 1
            elif not dict[p[1]]:
                return 0

        def play_game(log_name):
            game = Game() # TODO: add map path
            log_maker = LogMaker(log_name)
            reset()  

            game_data = Serializer.get(game)
            for player in p.values():
                player.put(str(game_data))

            ready_end_time = time.time() + ready_timeout
            game_end_time = time.time() + game_timeout
            is_ready = {player: False for player in p.values()}
            while time.time() < ready_end_time:
                for player in p.values():
                    if not is_ready[player]:
                        response = player.get()
                        if response is not None:
                            print(response, file=sys.stderr)
                        if response == 'READY':
                            is_ready[player] = True
                if all(is_ready.values()):
                    break
            else:
                return determine(is_ready)
                
            while time.time() < game_end_time:
                action = {player: None for player in p.values()}
                move_end_time = time.time() + move_timeout
                while time.time() < move_end_time <= game_end_time:
                    for player in p.values():
                        action[player] = player.get()
                    if all(action.values()):
                        break
                else:
                    return determine(action)
                
                print("RUCHY", action.values(), file=sys.stderr)
                log_maker.add_actions(*action.values())
                
                try:
                    action[p[0]] = str_to_action(action[p[0]], 0)
                except WrongMove:
                    return 1
                try:
                    action[p[1]] = str_to_action(action[p[1]], 1)
                except WrongMove:
                    return 0
                
                response = game.update(action[p[0]], action[p[1]])

                if response[0] == ErrorCode[1]:
                    log_maker.save()
                    return 0
                elif response[0] == ErrorCode[2]:
                    log_maker.save()
                    return 1
                elif "Tie" in response:
                    log_maker.save()
                    return 'TIE'
                
                game_data = Serializer.get(game)
                for player in p.values():
                    player.put(str(game_data))
                print("MAPA", file=sys.stderr)

            return "TIE"

                    
        for i in range(num_games):
            results.append(play_game(str(i)))
            for player in p.values():
                player.put('END')

        for player in p.values():
            player.put('BYE')
            player.kill()
        return results
