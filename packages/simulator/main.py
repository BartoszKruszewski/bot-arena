from .api import play

def Main():
    results = []
    for result in play("bot.py", "bot.py", 
                       num_games=100, 
                       map_name="example_map.json", 
                       log_name="pawel"):
        results.append(result)
    print(results)