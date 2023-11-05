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
    graphics_main()

if __name__ == '__main__':
    main()