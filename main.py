import sys
from os import remove, listdir

def game_logic_main():
    from packages.game_logic.main import TestRun

    TestRun()

def graphics_main():
    from packages.graphics.main import Main
    Main("example_log.txt")

def simulator_main():
    from packages.simulator.main import TestRun
    TestRun()

def main():
    if len(sys.argv) == 0:
        print('1 - game_logic')
        print('2 - graphics')
        print('3 - simulator')
        return
    
    if sys.argv[1] == '1':
        game_logic_main()
    elif sys.argv[1] == '2':
        graphics_main()
    elif sys.argv[1] == '3':
        simulator_main()
    elif sys.argv[1] == 'clear':
        for file in listdir('./logs'):
            if file != 'example_log.txt':
                remove('./logs/'+file)
        

if __name__ == '__main__':
    main()
