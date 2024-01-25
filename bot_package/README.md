# Python Bot Package
Celem tej paczki jest ułatwienie projektowania botów do Bot-Arena. Klasa `Bot` stanowi szablon do tworzenia kolejnych botów, umożliwiając dostosowywanie ich zachowania do różnych strategii gry.

## Bot Class

Klasa `Bot` jest szablonem do implementacji botów w Twoim programie.

### Atrybuty:
- `game_timeout (int)`: Czas dostępny na wykonanie ruchu w grze.
- `move_timeout (int)`: Czas dostępny na poruszanie się w grze.
- `ready_timeout (int)`: Czas oczekiwania na gotowość.
- `side (str)`: Strona, do której przypisany jest bot.
- `status (str)`: Bieżący status gry.
- `arena_properties (str)`: Właściwości areny gry.
---
### Metody:
- `preprocess(self) -> None`: Przygotowuje robota do rozpoczęcia gry.
- `make_move(self) -> str`: Wywołuje logikę robota w celu utworzenia ruchu.
- `post_move_action(self) -> None`: Wykonuje dodatkowe czynności po ruchu w pętli gry.
- `run(self) -> None`: Uruchamia główną pętlę robota.
---
### Przykładowe użycie:
```python
class MojBot(Bot):
    def preprocess(self):
        # Twoja niestandardowa logika przed rozpoczęciem gry

    def make_move(self):
        # Twoja niestandardowa logika generowania ruchu
        return Move.Wait()  # Domyślna akcja to oczekiwanie, zastąp to swoją logiką

    def post_move_action(self):
        # Twoja niestandardowa logika po ruchu

if __name__ == "__main__":
    moj_bot = MojBot()
    moj_bot.run()
```
---
**Uwaga:**

- Przesłoń dostarczone metody, aby dostosować zachowanie bota.
- Metody `receive_game_properties` i `receive_arena_properties` służą do odbierania zewnętrznego wejścia.
- Dostosuj format wejścia zgodnie z przykładem dla `arena_properties`.
- Klasa `Move` jest wykorzystywana do generowania ruchów w metodzie `make_move`.
- Dostosuj i rozbuduj szablon, aby zaimplementować unikalne strategie bota zgodnie z Twoimi potrzebami.
---
**Format Wejścia: JSON dla Arena Properties:**

Wartości `arena_properties` oczekiwane są w formacie JSON, jak przedstawiono poniżej:

```python
{
    'arena': {
        'base': {
            'left': [x_left, y_left],  # Współrzędne bazy po lewej stronie
            'right': [x_right, y_right]  # Współrzędne bazy po prawej stronie
        },
        'path': [
            [x1, y1],  # Współrzędne punktu na ścieżce
            [x2, y2],
            # ...
        ],
        'obstacles': [
            [ox1, oy1],  # Współrzędne przeszkody
            [ox2, oy2],
            # ...
        ],
        'map_size': [width, height]  # Rozmiar mapy
    },
    'players': {
        'left': {
            'buildings': {
                'turrets': [
                    [tx1, ty1],  # Współrzędne wieży
                    [tx2, ty2],
                    # ...
                ],
                'farms': [
                    [fx1, fy1],  # Współrzędne farmy
                    [fx2, fy2],
                    # ...
                ]
            },
            'units': [
                [ux1, uy1],  # Pozycja jednostki
                [ux2, uy2],
                # ...
            ],
            'gold': left_player_gold,  # Ilość złota dla gracza po lewej stronie
            'income': left_player_income  # Dochód gracza po lewej stronie
        },
        'right': {
            'buildings': {
                'turrets': [
                    # ...
                ],
                'farms': [
                    # ...
                ]
            },
            'units': [
                # ...
            ],
            'gold': right_player_gold,  # Ilość złota dla gracza po prawej stronie
            'income': right_player_income  # Dochód gracza po prawej stronie
        }
    }
}
```

## Move Class

Klasa `Move` reprezentuje różne akcje, które można wykonać w grze. Zawiera metody statyczne do oczekiwania, tworzenia jednostek i budowy struktur.

### Metody:
- `Wait(cls)`: Zwraca ciąg znaków reprezentujący akcję oczekiwania.
- `Spawn(cls, unit_type: str)`: Zwraca ciąg znaków reprezentujący akcję tworzenia jednostki z określonym typem.

#### Build:
- `Build.Turret(cls, x: int = 0, y: int = 0)`: Zwraca ciąg znaków reprezentujący budowę wieży na określonych współrzędnych.
- `Build.Farm(cls, x: int = 0, y: int = 0)`: Zwraca ciąg znaków reprezentujący budowę farmy na określonych współrzędnych.
---
### Przykładowe użycie:
```python
move_spawn = Move.Spawn("Archer")  # Reprezentuje tworzenie jednostki "Archer"
move_turret = Move.Build.Turret(3, 5)  # Reprezentuje budowę wieży na współrzędnych (3, 5)
move_farm = Move.Build.Farm(2, 4)  # Reprezentuje budowę farmy na współrzędnych (2, 4)
```

