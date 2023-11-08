import sys

def game_logic_main():
    from packages.game_logic.main import TestRun

    TestRun()

def graphics_main():
    from packages.graphics.main import Main
    Main()

def main():
    if len(sys.argv) == 0:
        print('1 - game_logic')
        print('2 - graphics')
        return
    
    if sys.argv[1] == '1':
        game_logic_main()
    elif sys.argv[1] == '2':
        graphics_main()

if __name__ == '__main__':
    main()