#include <iostream>
#include <random>
#include <algorithm>

std::pair<int, int> randomCoords() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 9);

    int x = dis(gen);
    int y = dis(gen);

    return std::make_pair(x, y);
}

std::string randomMove() {
    int x, y;
    char moveOptions[] = {'W', 'T', 'F', 'S'};
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 3);

    char move = moveOptions[dis(gen)];

    if (dis(gen) % 2 == 0 || move == 'W') {
        return "W";
    } else if (move == 'T' || move == 'F') {
        std::tie(x, y) = randomCoords();
        return std::string(1, move) + " " + std::to_string(x) + " " + std::to_string(y);
    } else if (move == 'S') {
        std::string unitOptions[] = {"swordsman", "archer"};
        return "S " + unitOptions[dis(gen) % 2];
    }

    return "";
}

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());

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
