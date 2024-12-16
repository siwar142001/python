import random

class Minesweeper:
    def __init__(self, difficulty="easy"):
        self.__difficulty = difficulty
        self.__rows, self.__columns, self.__bombs = self.__set_difficulty(difficulty)
        self.__matrix = [["0" for _ in range(self.__columns)] for _ in range(self.__rows)]

    def __set_difficulty(self, difficulty):
        if difficulty == "easy":
            return 9, 9, 10  # Grille 9x9 avec 10 bombes
        elif difficulty == "medium":
            return 16, 16, 40  # Grille 16x16 avec 40 bombes
        elif difficulty == "hard":
            return 16, 30, 99  # Grille 16x30 avec 99 bombes
        else:
            raise ValueError("Difficulté invalide. Utilisez 'easy', 'medium' ou 'hard'.")

    def __place_bombs(self):
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            i = random.randint(0, self.__rows - 1)
            j = random.randint(0, self.__columns - 1)
            if self.__matrix[i][j] != "B":
                self.__matrix[i][j] = "B"
                placed_bombs += 1

    def __calculate_numbers(self):
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] == "B":
                    continue

                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        new_i = i + x
                        new_j = j + y
                        if 0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][new_j] == "B":
                            count += 1
                self.__matrix[i][j] = str(count)

    def __display(self):
        for row in self.__matrix:
            print(" ".join(row))

    def play(self):
        self.__place_bombs()
        self.__calculate_numbers()
        self.__display()

# Programme principal
if __name__ == "__main__":
    difficulty = "easy"  # Choisir 'easy', 'medium' ou 'hard'
    game = Minesweeper(difficulty)
    game.play()
