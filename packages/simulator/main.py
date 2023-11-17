import os
from .game_controller import GameController

def choose_bot(folder_path, prompt):
    file_list = [file_name for file_name in os.listdir(folder_path) if not file_name.endswith("__pycache__")]

    for i, file_name in enumerate(file_list, start=1):
        print(f"{i}. {file_name}")
    while True:
        selected_index = int(input(prompt))

        if 1 <= selected_index <= len(file_list):
            selected_file = file_list[selected_index - 1]
            return os.path.join(folder_path, selected_file)
        else:
            print("Podano nieprawidłową liczbę.")

def TestRun():
    folder_path = "packages/simulator/bots"

    bot1_path = choose_bot(folder_path, "Wybierz bota 1: ")
    bot2_path = choose_bot(folder_path, "Wybierz bota 2: ")

    game = GameController(bot1_path, bot2_path)
    game.run()

if __name__ == '__main__':
    TestRun()
