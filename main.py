import sys

def game_logic_main():
    from packages.game_logic.main import TestRun

    TestRun()

def graphics_main():
    from packages.graphics.main import Main
    Main()

def simulator_main():
    pass

def main():
    if len(sys.argv) == 0:
        print('No arguments')
        return
    
    if sys.argv[1] == '1':
        game_logic_main()
    if sys.argv[1] == '2':
        graphics_main()
    if sys.argv[1] == '3':
        simulator_main()

if __name__ == '__main__':
    main()