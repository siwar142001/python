
import random

class Minesweeper:
    def __init__(self, rows, columns, bombs):
        """
        Initialise une nouvelle instance de la classe Minesweeper.
        :param rows: Nombre de lignes de la grille.
        :param columns: Nombre de colonnes de la grille.
        :param bombs: Nombre de bombes sur le champ.
        """
        self.__rows = rows
        self.__columns = columns
        self.__bombs = bombs
        self.__matrix = [["0" for _ in range(columns)] for _ in range(rows)]
        self.__display_matrix = [[" " for _ in range(columns)] for _ in range(rows)]
        self.__flags = 0
        self.__first_click = True

    def __place_bombs(self, first_click_row, first_click_col):
        """
        Place les bombes aléatoirement sur la grille tout en évitant
        la case initiale cliquée par l'utilisateur.
        :param first_click_row: Ligne du premier clic.
        :param first_click_col: Colonne du premier clic.
        """
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            i = random.randint(0, self.__rows - 1)
            j = random.randint(0, self.__columns - 1)
            # Vérifie que la case n'est pas la case initiale du clic
            if (i, j) != (first_click_row, first_click_col) and self.__matrix[i][j] != "B":
                self.__matrix[i][j] = "B"
                placed_bombs += 1

        self.__calculate_numbers()

        # Si la case initiale n'est pas "0", déplacer les bombes
        while self.__matrix[first_click_row][first_click_col] != "0":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_i = first_click_row + x
                    new_j = first_click_col + y
                    if (0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][new_j] == "B"):
                        self.__matrix[new_i][new_j] = "0"
                        while True:
                            i = random.randint(0, self.__rows - 1)
                            j = random.randint(0, self.__columns - 1)
                            if self.__matrix[i][j] == "0" and (i, j) != (first_click_row, first_click_col):
                                self.__matrix[i][j] = "B"
                                break
            self.__calculate_numbers()

    def __calculate_numbers(self):
        """
        Calcule le nombre de bombes adjacentes pour chaque case de la grille
        et met à jour la grille en conséquence.
        """
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] == "B":
                    continue

                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        new_i = i + x
                        new_j = j + y
                        if 0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][
                            new_j] == "B":
                            count += 1
                self.__matrix[i][j] = str(count)

    def __reveal_cells(self, row, col):
        """
        Révèle les cellules adjacentes de manière récursive si aucune bombe
        n'est présente autour de la case initiale.
        :param row: Ligne de la cellule à révéler.
        :param col: Colonne de la cellule à révéler.
        """
        if not (0 <= row < self.__rows and 0 <= col < self.__columns) or self.__display_matrix[row][col] != " ":
            return

        self.__display_matrix[row][col] = self.__matrix[row][col]

        if self.__matrix[row][col] == "0":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        self.__reveal_cells(row + x, col + y)

    def display_solution(self):
        """
        Affiche la matrice complète contenant les solutions (bombes et chiffres).
        """
        print("--- Solution ---")
        for row in self.__matrix:
            print(" ".join(row))

    def click_cell(self, row, col):
        """
        Gère le clic sur une cellule de la grille.
        :param row: Ligne de la cellule cliquée.
        :param col: Colonne de la cellule cliquée.
        :return: "lost" si une bombe est cliquée, "continue" sinon, ou "flagged" si un drapeau est présent.
        """

        if self.__display_matrix[row][col] == "F":
            return "flagged"  # Ne pas révéler une case marquée par un drapeau

        if self.__first_click:
            self.__place_bombs(row, col)  # Place les bombes avant le premier clic
            self.__calculate_numbers()
            self.__first_click = False
            self.display_solution()  # Affiche la solution

        if self.__matrix[row][col] == "B":
            return "lost"

        self.__reveal_cells(row, col)
        return "continue"

    def toggle_flag(self, row, col):
        """
        Ajoute ou retire un drapeau sur une cellule spécifique.
        :param row: Ligne de la cellule.
        :param col: Colonne de la cellule.
        """

        if self.__display_matrix[row][col] == " ":
            self.__display_matrix[row][col] = "\U0001F6A9"  # Drapeau rouge
        elif self.__display_matrix[row][col] == "\U0001F6A9":
            self.__display_matrix[row][col] = " "

    def is_won(self):
        """
        Vérifie si le joueur a gagné la partie.
        Une partie est gagnée si toutes les cases sans bombes sont révélées
        et toutes les cases contenant des bombes sont soit non révélées, soit marquées avec un drapeau.
        :return: True si la partie est gagnée, False sinon.
        """
        for i in range(self.__rows):
            for j in range(self.__columns):
                # Si une case sans bombe n'est pas révélée, le joueur n'a pas gagné
                if self.__matrix[i][j] != "B" and self.__display_matrix[i][j] == " ":
                    return False
                # Si une case contenant une bombe est révélée sans drapeau, le joueur n'a pas gagné
                if self.__matrix[i][j] == "B" and self.__display_matrix[i][j] not in [" ", "\U0001F6A9"]:
                    return False
        return True

    def get_display_matrix(self):
        """
        Retourne la matrice actuelle à afficher pour le joueur.
        :return: Matrice affichée.
        """
        return self.__display_matrix

    def save_first_click(self, row, col):
        """
        Enregistre le premier clic pour une grille donnée.
        :param row: Ligne du premier clic.
        :param col: Colonne du premier clic.
        """
        self.first_click_row = row
        self.first_click_col = col

    def load_saved_grid(self, grid_data):
        """
        Charge une grille enregistrée et restaure les paramètres initiaux.
        :param grid_data: Données de la grille.
        """
        self.__matrix = grid_data
        self.__first_click = False  # Désactive la génération aléatoire
