#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

using namespace std;

int random_num(int range) {
    return rand() % (range + 1);
}

std::string randomMove() {
    int x, y;
    vector<char> moveOptions = {'W', 'T', 'F', 'S'};

    char move = moveOptions[random_num(moveOptions.size() - 1)];

    if (random_num(100) < 50 || move == 'W') {
        return "W";

    } else if (move == 'T') {
        x = random_num(9);
        y = random_num(9);
        return "T " + to_string(x) + " " + to_string(y);

    } else if (move == 'F') {
        x = random_num(9);
        y = random_num(9);
        return "F " + to_string(x) + " " + to_string(y);

    } else if (move == 'S') {
        vector<string> unitOptions = {"swordsman", "archer"};
        return "S " + unitOptions[random_num(unitOptions.size() - 1)];
    }

    return "";
}

int main() {
    while (true) {
        string settings;
        string map;

        getline(std::cin, settings);
        getline(std::cin, map);

        cerr << "READY" << endl;
        cout << "READY" << endl;

        while (true) {
            string move = randomMove();
            cout << move << endl;

            string message;
            getline(cin, message);

            if (message == "END") {
                break;
            }
        }
    }

    return 0;
}
