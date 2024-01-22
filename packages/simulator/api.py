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

def play(name1, name2, num_games, map_name, log_name="logs",
        ready_timeout=100, move_timeout=100, game_timeout=600):
        
        p = {}

        def reset():
            if not p:
                for player in p.values():
                    player.kill()
                p[0] = Bot(name1)
                p[1] = Bot(name2)
           
            for i, player in enumerate(p.values()):
                # send settings to bots
                player.put(f"{game_timeout} {move_timeout} {ready_timeout} {'left' if i == 0 else 'right'}")
                player.put(map_name)
                player.total_time = 0.0

        results = []

        def determine(dict : dict[int, bool]):
            if not dict[p[0]] and not dict[p[1]]:
                return 'TIE'
            elif not dict[p[0]]:
                return 1
            elif not dict[p[1]]:
                return 0

        def play_game(log_name, log_number, map_name):
            game = Game(map_name) 
            log_maker = LogMaker(log_name, log_number)
            reset()  

            ready_end_time = time.time() + ready_timeout
            game_end_time = time.time() + game_timeout
            is_ready = {player: False for player in p.values()}
            while time.time() < ready_end_time:
                for player in p.values():
                    if not is_ready[player]:
                        response = player.get()
                        if response == 'READY':
                            is_ready[player] = True
                if all(is_ready.values()):
                    break
            else:
                print(__name__, "end by ready timeout", file=sys.stderr)
                log_maker.save("TIE", map_name, name1, name2)
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
                    print(__name__, "end by move timeout", file=sys.stderr)
                    log_maker.save("TIE", map_name, name1, name2)
                    return determine(action)
                
                # print("RUCHY", action.values(), file=sys.stderr)
                log_maker.add_actions(*action.values())
                
                try:
                    action[p[0]] = str_to_action(action[p[0]], 0)
                except WrongMove:
                    print(__name__, "end by wrong move", file=sys.stderr)
                    return 1
                try:
                    action[p[1]] = str_to_action(action[p[1]], 1)
                except WrongMove:
                    print(__name__, "end by wrong move", file=sys.stderr)
                    return 0
                
                response = game.update(action[p[0]], action[p[1]])

                if response[0] == ErrorCode[1]:
                    log_maker.save("0", map_name, name1, name2)
                    return 0
                elif response[0] == ErrorCode[2]:
                    log_maker.save("1", map_name, name1, name2)
                    return 1
                elif "Tie" in response:
                    log_maker.save("TIE", map_name, name1, name2)
                    print(__name__, "end by tie", file=sys.stderr)
                    return 'TIE'
                
                game_data = Serializer.get(game)
                actions = f"{action[p[0]]} | {action[p[1]]}"
                for player in p.values():
                    player.put(actions)

            return "TIE"

        LogMaker.clear(log_name)
        for i in range(num_games):
            yield(play_game(log_name, str(i), map_name))
            for player in p.values():
                player.put('END')

        for player in p.values():
            player.put('BYE')
            player.kill()
        return results
