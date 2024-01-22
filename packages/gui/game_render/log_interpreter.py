from os import listdir, path
from packages.game_logic.actions import str_to_actions, Wait
from packages import LOGS_DIRECTORY

class LogInterpreter:
    '''Changes .txt file to list[tuple[Action, Action]]
    
    '''

    def __init__(self, log_path: str) -> None:
        self.log = []
        self.map_name = None
        self.player1_name = None
        self.player2_name = None

        log_path = path.join(LOGS_DIRECTORY, log_path)
        self.__load_log(log_path)
        self.__parse_log()

        self.index = 0
         
        
    def __load_log(self, log_path: str):
        with open(log_path, "r") as log:
            self.log = log.readlines()
    
    def __parse_log(self):
        self.log = [line.strip().split() for line in self.log]
        action_log = []
        
        self.map_name = self.log[0][0][4:]
        self.player1_name = self.log[1][0][8:]
        self.player2_name = self.log[2][0][8:]

        for line in self.log[3:]:
            if line[0] == "#": continue

            left_action, right_action = str_to_actions(line)
           
            action_log.append((left_action, right_action))

        self.log = action_log

    def get_next_actions(self) -> tuple:
        if self.index >= len(self.log):
            return (Wait('left'), Wait('right'))
        
        actions = self.log[self.index]
        self.index += 1

        return actions
    
    def get_index(self):
        return self.index
    
    def get_map_name(self):
        return self.map_name
        