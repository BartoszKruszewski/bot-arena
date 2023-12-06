from .api import play

def main():
    print(play("bot.py", "bot.cpp", num_games=3))