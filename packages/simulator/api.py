import time
import sys

from .bot import Bot
from .serializer import Serializer
from .log_maker import LogMaker
from packages.game_logic.game import Game, ErrorCode
from packages.game_logic.actions import Wait, BuildFarm, BuildTurret, SpawnSoldier

# Define a custom exception for incorrect moves
class WrongMove(Exception):
    pass

# Function to convert a string into a corresponding action object
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

# Main function for playing multiple games
def play(name1, name2, num_games, map_name, log_name="logs",
        ready_timeout=100, move_timeout=100, game_timeout=600):
        
    # Dictionary to store player instances
    p = {}

    # Initialize the game object
    game = Game(map_name) 

    # Function to reset the game state and initialize players if not already done
    def reset():
        if not p:
            for player in p.values():
                player.kill()
            p[0] = Bot(name1)
            p[1] = Bot(name2)

        for i, player in enumerate(p.values()):
            # Send settings to bots
            player.put(f"{game_timeout} {move_timeout} {ready_timeout} {'left' if i == 0 else 'right'}")

            game_data = Serializer.get_json(game)
            player.put(game_data)
            player.total_time = 0.0

    # List to store results of each game
    results = []

    # Function to determine the winner of a game based on the player's state
    def determine(dict : dict[int, bool]):
        if not dict[p[0]] and not dict[p[1]]:
            return 'TIE'
        elif not dict[p[0]]:
            return 1
        elif not dict[p[1]]:
            return 0

    # Function to play a single game
    def play_game(log_name, log_number, map_name):
        # Initialize the game and log maker
        game = Game(map_name) 
        log_maker = LogMaker(log_name, log_number)
        reset()  

        # Set timeout values
        ready_end_time = time.time() + ready_timeout
        game_end_time = time.time() + game_timeout
        is_ready = {player: False for player in p.values()}

        # Wait for players to be ready
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
            
        # Play the game until timeout
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
            
            # Add actions to the log
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
            
            # Update the game state and get the response
            response = game.update(action[p[0]], action[p[1]])

            # Check for game end conditions and save the log
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
            
            # Send game data to players
            game_data = Serializer.get_json(game)
            actions = f"{action[p[0]]} | {action[p[1]]}"
            for player in p.values():
                player.put(actions)
                player.put(game_data)

        return "TIE"

    # Play the specified number of games
    LogMaker.clear(log_name)
    for i in range(num_games):
        yield(play_game(log_name, str(i), map_name))
        for player in p.values():
            player.put('END')

    # End the game and kill player processes
    for player in p.values():
        player.put('BYE')
        player.kill()
    return results