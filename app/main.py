from typing import List


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    ships = []

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        if start[0] < end[0]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))
        if start[1] < end[1]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        self.ships.append(self)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck
        return None

    def get_ship_decks(self) -> List[Deck]:
        result = []
        for deck in self.decks:
            result.append((deck.row, deck.column))
        return result

    def fire(self, row: int, column: int) -> None:
        deck_hit = self.get_deck(row, column)
        if deck_hit.is_alive:
            deck_hit.is_alive = False
        decks_of_ship = []
        for deck in self.decks:
            decks_of_ship.append(deck.is_alive)
        if not any(decks_of_ship):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.get_ship_decks():
                self.field.update({deck: new_ship})

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        else:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"


def print_field(battleship: Battleship) -> None:
    print("\nBATTLESHIP:\n")
    list_of_decks = []
    hit_decks = []
    for ship in battleship.field.values():
        for deck in ship.decks:
            if deck.is_alive:
                list_of_decks.append((deck.row, deck.column))
            if not deck.is_alive:
                hit_decks.append((deck.row, deck.column))
    for row in range(0, 10):
        row_to_print = ""
        for column in range(0, 10):
            if (row, column) in hit_decks:
                row_to_print += " X "
                continue
            if (row, column) in list_of_decks:
                row_to_print += " □ "
                continue
            row_to_print += " - "
        print(row_to_print)
