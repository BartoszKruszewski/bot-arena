def game_logic_main():
    from packages.game_logic.main import TestRun

    TestRun()

def graphics_main():
    pass

def simulator_main():
    pass

def main():
    import sys
    if len(sys.argv) == 0:
        print('No arguments')
        return
    
    if sys.argv[1] == '1':
        game_logic_main()
    if sys.argv[1] == '2':
        graphics_main()
    if sys.argv[1] == '3':
        simulator_main()