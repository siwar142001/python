#import pygame
import random
import tkinter as tk
from tkinter import messagebox
import pygame



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
        print("\n--- Solution ---")
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



class MinesweeperApp:
    def __init__(self, root):
        """
        Initialise l'application graphique Tkinter pour le jeu du démineur.
        :param root: Fenêtre principale Tkinter.
        """
        self.root = root
        self.root.title("Minesweeper")

        self.game = None
        self.buttons = []

        self.__create_home_menu()

    def __create_home_menu(self):
        """
        Crée le menu d'accueil principal.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#AED6F1")

        home_frame = tk.Frame(self.root)
        home_frame.pack(pady=50)



        tk.Label(home_frame, text="Bienvenue sur Minesweeper !", font=("Arial", 50),fg='#3498DB').pack(pady=20)

        tk.Button(home_frame, text="Commencer le jeu", font=("Arial", 50),bg='#3498DB',fg='#ECF0F1', command=self.__create_difficulty_menu).pack(pady=15)

        tk.Button(home_frame, text="Quitter", font=("Arial", 30),bg='#E74C3C',fg='#ECF0F1', command=self.root.quit).pack(pady=50)




        pygame.mixer.init()
        pygame.mixer.music.load("test.mp3")
        pygame.mixer.music.play(-1)

    def __create_difficulty_menu(self):
        """
        Crée l'interface de sélection de difficulté.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=100)

        tk.Label(difficulty_frame, text="Choisissez une difficulté", font=("Arial", 60),bg=('#AED6F1'),fg='#3498DB').pack(pady=0)

        tk.Button(difficulty_frame, text="Facile (9x9, 10 bombes)", font=("Arial", 20),bg=('#FADBD8'),
                  command=lambda: self.__start_game(9, 9, 10)).pack(pady=20)
        tk.Button(difficulty_frame, text="Moyen (16x16, 40 bombes)", font=("Arial", 20),bg=('#FADBD8'),
                  command=lambda: self.__start_game(16, 16, 40)).pack(pady=20)
        tk.Button(difficulty_frame, text="Difficile (20x24, 99 bombes)", font=("Arial", 20),bg=('#FADBD8'),
                  command=lambda: self.__start_game(20, 24, 99)).pack(pady=20)

        tk.Button(difficulty_frame, text="Retour", font=("Arial", 20),bg=('#FADBD8'), command=self.__create_home_menu).pack(pady=10)

    def __start_game(self, rows, columns, bombs):
        """
        Initialise une nouvelle partie avec la difficulté choisie.
        :param rows: Nombre de lignes de la grille.
        :param columns: Nombre de colonnes de la grille.
        :param bombs: Nombre de bombes sur la grille.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        self.game = Minesweeper(rows, columns, bombs)
        self.buttons = []



        for i in range(rows):
            row_buttons = []
            for j in range(columns):
                btn = tk.Button(self.root, text=" ", width=3, height=1)
                btn.grid(row=i, column=j)

                # Gestion des clics gauche et droit
                btn.bind("<Button-1>", lambda e, r=i, c=j: self.__on_click(e, r, c))
                btn.bind("<Button-2>", lambda e, r=i, c=j: self.__on_right_click(e, r, c))

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def __on_click(self, event, row, col):
        """
        Gère un clic gauche sur une cellule de la grille.
        :param event: Événement Tkinter.
        :param row: Ligne de la cellule cliquée.
        :param col: Colonne de la cellule cliquée.
        """
        result = self.game.click_cell(row, col)
        self.__update_buttons()

        if result == "lost":
            messagebox.showinfo("Game Over", "Vous avez cliqué sur une mine! Partie terminée.")
            pygame.mixer.quit()
            self.root.destroy()
        elif self.game.is_won():
            messagebox.showinfo("Félicitations", "Vous avez gagné!")
            pygame.mixer.quit()
            self.root.destroy()

    def __on_right_click(self, event, row, col):
        """
        Gère un clic droit pour ajouter ou retirer un drapeau sur une cellule.
        :param event: Événement Tkinter.
        :param row: Ligne de la cellule.
        :param col: Colonne de la cellule.
        """
        self.game.toggle_flag(row, col)
        self.__update_buttons()

    def __update_buttons(self):
        """
        Met à jour l'affichage des boutons en fonction de la matrice du jeu.
        """
        display_matrix = self.game.get_display_matrix()
        for i, row in enumerate(display_matrix):
            for j, value in enumerate(row):
                self.buttons[i][j].config(text=value)


if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
