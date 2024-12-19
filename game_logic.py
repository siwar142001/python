import random
import json  # Pour la sauvegarde en format JSON

class Minesweeper:
    def __init__(self, rows, columns, bombs):
        self.__rows = rows
        self.__columns = columns
        self.__bombs = bombs
        self.__matrix = [["0" for _ in range(columns)] for _ in range(rows)]
        self.__display_matrix = [[" " for _ in range(columns)] for _ in range(rows)]
        self.__flags = 0
        self.__first_click = True
        self.first_click_row = -1
        self.first_click_col = -1

    def __place_bombs(self, first_click_row, first_click_col):
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            i = random.randint(0, self.__rows - 1)
            j = random.randint(0, self.__columns - 1)
            if (i, j) != (first_click_row, first_click_col) and self.__matrix[i][j] != "B":
                self.__matrix[i][j] = "B"
                placed_bombs += 1
        self.__calculate_numbers()

    def __calculate_numbers(self):
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] == "B":
                    continue
                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        new_i = i + x
                        new_j = j + y
                        if 0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][new_j] == "B":
                            count += 1
                self.__matrix[i][j] = str(count)

    def __reveal_cells(self, row, col):
        if not (0 <= row < self.__rows and 0 <= col < self.__columns) or self.__display_matrix[row][col] != " ":
            return
        self.__display_matrix[row][col] = self.__matrix[row][col]
        if self.__matrix[row][col] == "0":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        self.__reveal_cells(row + x, col + y)

    def display_solution(self):
        print("--- Solution ---")
        for row in self.__matrix:
            print(" ".join(row))

    def click_cell(self, row, col):
        if self.__display_matrix[row][col] == "F":
            return "flagged"

        if self.__first_click:
            self.first_click_row = row
            self.first_click_col = col
            self.__place_bombs(row, col)
            self.__calculate_numbers()
            self.__first_click = False
            self.save_game()  # Sauvegarde après le premier clic
        if self.__matrix[row][col] == "B":
            return "lost"
        self.__reveal_cells(row, col)
        return "continue"

    def toggle_flag(self, row, col):
        if self.__display_matrix[row][col] == " ":
            self.__display_matrix[row][col] = "\U0001F6A9"
        elif self.__display_matrix[row][col] == "\U0001F6A9":
            self.__display_matrix[row][col] = " "

    def is_won(self):
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] != "B" and self.__display_matrix[i][j] == " ":
                    return False
                if self.__matrix[i][j] == "B" and self.__display_matrix[i][j] not in [" ", "\U0001F6A9"]:
                    return False
        return True

    def get_display_matrix(self):
        return self.__display_matrix

    def save_game(self):
        game_state = {
            "matrix": self.__matrix,
            "display_matrix": self.__display_matrix,
            "first_click_row": self.first_click_row,
            "first_click_col": self.first_click_col,
            "flags": self.__flags,
            "first_click": self.__first_click
        }
        with open("saved_game.json", "w") as f:
            json.dump(game_state, f)

    def load_game(self):
        try:
            with open("saved_game.json", "r") as f:
                game_state = json.load(f)
                self.__matrix = game_state["matrix"]
                self.__display_matrix = game_state["display_matrix"]
                self.first_click_row = game_state["first_click_row"]
                self.first_click_col = game_state["first_click_col"]
                self.__flags = game_state["flags"]
                self.__first_click = game_state["first_click"]
        except FileNotFoundError:
            print("Aucun jeu sauvegardé trouvé.")
