from os import path

PACKAGE_DIRECTORY = path.dirname(path.abspath(__file__))
LOGS_DIRECTORY = path.join(path.dirname(PACKAGE_DIRECTORY), "logs")
MAPS_DIRECTORY = path.join(path.dirname(PACKAGE_DIRECTORY), "maps")