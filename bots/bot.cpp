#include <iostream>
#include <cstdlib>
#include <ctime>
#include <algorithm>

std::pair<int, int> randomCoords() {
    int x = std::rand() % 10;
    int y = std::rand() % 10;
    return std::make_pair(x, y);
}

std::string randomMove() {
    int x, y;
    char moveOptions[] = {'W', 'T', 'F', 'S'};
    char move = moveOptions[std::rand() % 4];

    if (std::rand() % 2 == 0 || move == 'W') {
        return "W";
    } else if (move == 'T') {
        std::tie(x, y) = randomCoords();
        return "T " + std::to_string(x) + " " + std::to_string(y);
    } else if (move == 'F') {
        std::tie(x, y) = randomCoords();
        return "F " + std::to_string(x) + " " + std::to_string(y);
    } else if (move == 'S') {
        std::string unitOptions[] = {"swordsman", "archer"};
        return "S " + unitOptions[std::rand() % 2];
    }

    return "";
}

int main() {
    std::srand(std::time(0));

    std::string settings;
    std::getline(std::cin, settings);

    std::string map;
    std::getline(std::cin, map);

    while (true) {
        std::cerr << "READY" << std::endl;
        std::cout << "READY" << std::endl;

        while (true) {
            std::string move = randomMove();
            std::cout << move << std::endl;

            std::string message;
            std::getline(std::cin, message);

            if (message == "END") {
                break;
            }
        }
    }

    return 0;
}
