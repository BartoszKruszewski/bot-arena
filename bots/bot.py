import random
import sys

def random_cords():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return x, y

def random_move():
    move = random.choice(['W', 'T', 'F', 'S'])
    
    if random.uniform(0, 1) < 0.5 or move == 'W':
        return f'W'
    elif move == 'T':
        x, y = random_cords()
        return f'T {x} {y}'
    elif move == 'F':
        x, y = random_cords()
        return f'F {x} {y}'
    elif move == 'S':
        return f'S {random.choice(["swordsman", "archer"])}'
    
while True:
    settings = input()
    map = input()

    print("READY", file=sys.stderr)
    print("READY")

    i = 0
    while i < 2:
        i += 1
        move = random_move()
        print(move)
        message = input()
        if message == "END":
            break

    


