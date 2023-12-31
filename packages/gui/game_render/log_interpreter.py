from os import listdir
from packages.game_logic.actions import Action, BuildTurret, BuildFarm, SpawnSoldier, Wait

class LogInterpreter:
    '''Changes .txt file to list[tuple[Action, Action]]
    
    '''
    letter_to_action = {
        'W': Wait,
        'S': SpawnSoldier,
        'T': BuildTurret,
        'F': BuildFarm
    }

    def __init__(self, log_path: str) -> None:
        self.log = []

        self.__load_log(log_path)
        self.__parse_log()

        self.index = 0
        
    def __load_log(self, log_path: str):
        with open(log_path, "r") as log:
            self.log = log.readlines()
    
    def __parse_log(self):
        self.log = [line.strip().split() for line in self.log]
        action_log = []
        for line in self.log:
            if line[0] == "#": continue

            left_side, right_side = line[:line.index("|")], line[line.index("|")+1:]
            left_action, right_action = left_side[0], right_side[0]
            left_args, right_args = ["left"] + left_side[1:], ["right"] + right_side[1:]
           
            left_action = LogInterpreter.letter_to_action[left_action[0]]
            right_action = LogInterpreter.letter_to_action[right_action[0]]

            left_action = left_action(*left_args)
            right_action = right_action(*right_args)
           
            action_log.append((left_action, right_action))

        self.log = action_log

    def get_next_actions(self) -> tuple[Action, Action]:
        if self.index >= len(self.log):
            return (Wait('left'), Wait('right'))
        
        actions = self.log[self.index]
        self.index += 1

        return actions
        