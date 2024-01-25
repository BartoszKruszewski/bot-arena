import json
from typing import final
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bot_package.move import Move

class Bot():
    """
    Template class for bot.

    Attributes:
    - game_timeout (int): Time available for making a move in the game.
    - move_timeout (int): Time available for movement in the game.
    - ready_timeout (int): Time for waiting for readiness.
    - side (str): The side to which the bot is assigned.
    - status (str): Current status of game.
    - arena_properties (str): Properties of the game arena.
    """

    def __init__(self): 
        # Initialize bot attributes
        self.game_timeout = None
        self.move_timeout = None
        self.ready_timeout = None
        self.side = None
        self.status = None
        self.arena_properties = None
    

    def preprocess(self) -> None:
        """
        Prepares the robot for the start of the game.
        -------------------------------------------------------------
        Note: This method should be overridden by the user to add custom functionality.
        """
        # Additional procces before starting game can be added here if needed
        pass
    
    
    def make_move(self) -> str:
        """
        Invokes the robot's logic to create a move.
        -------------------------------------------------------------
        Note: This method should be overridden by the user to include
        logic of the robot to generate moves in the game.
        """
        # Additional setup logic can be added here if needed
        # Use the Move class to generate a move

        return Move.Wait()  # Default action is to wait, replace this with your logic

    def post_move_action(self) -> None:
        """
        Perform additional actions after move in the game loop.
        -------------------------------------------------------------
        Note: This method should be overridden by the user to add custom functionality.
        """
        # Additional post move action can be added here if needed
        pass

    @final
    def run(self) -> None:
        """
        Runs the main loop of the robot.

        In this method, the robot prepares for the game,
        then enters the main loop where it makes moves
        and receives the game status until the game ends.
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        # Receive initial game and arena properties
        self.receive_game_properties()
        self.receive_arena_properties()

        # Initial preparation
        self.preprocess()
        self.send_message("READY")

        while True:
            # Make a move and send it to the game
            move = self.make_move()
            self.send_move(move)

            # Receive and process the game status
            status = self.receive_status()

            # Check if the game has ended
            if status == "END":
                break

            # Receive and update arena properties after made moves by both sides    
            self.receive_arena_properties()

            # Perform additional actions after a move
            self.post_move_action()

    @final
    def receive_game_properties(self) -> None:
        """
        Receives arena properties from the game.
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        game_timeout, move_timeout, ready_timeout, side = input().split()
        
        # Convert received values to appropriate types and assign to attributes
        self.game_timeout = game_timeout
        self.move_timeout = move_timeout
        self.ready_timeout = ready_timeout
        self.side = side

    @final
    def receive_arena_properties(self) -> dict:
        """
        Receives arena properties from the game.
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        # Receive and assign arena properties in format of json
        json_input_str = input()

        # Deserialize JSON and assign to self.arena_properties
        self.arena_properties = json.loads(json_input_str)


    @final
    def receive_status(self) -> str:
        """
        Receives the current game status from the game.

        The game status can be "END" for simulation end or last move from each side in the format "{left move} | {right move}".
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        # Receive and assign game status
        self.status = input()
        return self.status

    @final
    def send_move(self, move: str = Move.Wait()) -> None:
        """
        Sends the robot's move to the game.
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        # Print the move to standart output
        self.send_message(move)

    @final
    def send_message(self, message: str = '') -> None:
        """
        Sends the bot's message to the game.
        ----------------------------------------------------------------------------------
        Note: This method is marked as @final, indicating that it should not be overridden
        in any subclasses. Changing its behavior in subclasses can result in errors.
        """
        # Print the move to standart output
        print(message)

