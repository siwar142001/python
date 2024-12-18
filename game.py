import random
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

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
                        if 0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][new_j] == "B":
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

            self.display_solution() # Affiche la solution

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
        Vérifie si le joueur a gagné la partie en marquant toutes les bombes
        et en révélant toutes les autres cases.
        :return: True si le joueur a gagné, False sinon.
        """
        # Vérifie si toutes les bombes ont été marquées et si toutes les cases sans bombe ont été révélées
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] == "B" and self.__display_matrix[i][j] != "\U0001F6A9":  # Bombe non marquée
                    return False
                if self.__matrix[i][j] != "B" and self.__display_matrix[i][j] == " ":  # Case non-bombe non révélée
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

        self.__create_menu()

    def start_game(self, rows, columns, bombs):
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
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.__on_right_click(e, r, c))

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def __create_menu(self):
        """
        Crée le menu principal pour choisir la difficulté.
        """

        ### Fonction de la page 'Difficulté' ###
        def choix_difficulte():
            print("Choisissez votre difficulté :")

            # Efface les widgets existants
            for widget in fenetre.winfo_children():
                widget.destroy()

            # Création des Frames
            frame_retour = Frame(fenetre, bg="grey")  # Frame pour le bouton Retour
            frame_retour.pack(fill="x", anchor="nw", pady=10, padx=10)  # En haut à gauche

            frame_titre = Frame(fenetre, bg="grey")  # Frame pour le titre
            frame_titre.pack(pady=20)

            frame_difficulte = Frame(fenetre, bg="grey")  # Frame pour les boutons de difficulté
            frame_difficulte.pack(expand=True, pady=20)  # Centré verticalement

            # Boutons
            retour = Button(frame_retour, text="Retour", font=("Cambria", 20), bg='purple', fg='black',
                            command=retour_accueil)
            retour.pack(anchor="nw")  # Bouton "Retour" aligné en haut à gauche

            # Titre de la difficulté
            titre = Label(frame_titre, text="Choisissez la difficulté du niveau", font=("Cambria", 30), bg='grey',
                          fg='white')
            titre.pack()


            # Boutons de difficulté
            facile = Button(frame_difficulte, text="Facile", font=("Cambria", 40), bg='green', fg='black',
                            command=lambda: self.start_game(8, 8, 10))
            moyen = Button(frame_difficulte, text="Moyen", font=("Cambria", 40), bg='orange', fg='black',
                           command=lambda: self.start_game(16, 16, 40))
            difficile = Button(frame_difficulte, text="Difficile", font=("Cambria", 40), bg='red', fg='black',
                            command=lambda: self.start_game(24, 24, 99))

            # Placement horizontal des boutons de difficulté
            facile.grid(row=0, column=0, padx=20)  # Espacement horizontal entre les boutons
            moyen.grid(row=0, column=1, padx=20)
            difficile.grid(row=0, column=2, padx=20)

        ### Fonction pour quitter le jeu ###
        def quitter_jeux():
            print("Extinction du jeu...")
            fenetre.destroy()

        ### Fonction de création du tableau 'score' ###
        def affiche_score():
            print("Affichage du score...")

            # Efface les widgets existants
            for widget in fenetre.winfo_children():
                widget.destroy()

            # Création du tableau
            tableau = ttk.Treeview(fenetre, columns=("Nom", "Date", "Score"), show="headings")

            tableau.heading("Nom", text="Nom")
            tableau.heading("Date", text="Date")  # Ajout des colonnes dans le tableau
            tableau.heading("Score", text="Score")

            tableau.column("Nom", width=150, anchor=CENTER)
            tableau.column("Date", width=100, anchor=CENTER)
            tableau.column("Score", width=150, anchor=CENTER)

            # Données quelconques
            donnees = [('Raphaël', '16-12-2024', 255), ('Siwar', '15-12-2024', 95), ('Ines', '13-12-2024', 1)]

            # Insertion des données dans le tableau
            for ligne in donnees:
                tableau.insert("", END, values=ligne)

            tableau.pack(pady=20)

            # Bouton Retour
            retour = Button(fenetre, text="Retour", font=("Cambria", 20), bg='purple', fg='black',
                            command=retour_accueil)
            retour.pack(pady=20)

        ### Fonction pour revenir à l'accueil ###
        def retour_accueil():
            print("Retour à la page d'accueil...")

            # Efface les widgets existants
            for widget in fenetre.winfo_children():
                widget.destroy()

            # Page Accueil
            demineur = Label(fenetre, text="Démineur", font=("Cambria", 75), bg='grey', fg='pink')
            jouer = Button(fenetre, text="Jouer", font=("Cambria", 40), bg='pink', fg='white', command=choix_difficulte)
            sub_score = Button(fenetre, text="Score", font=("Cambria", 40), bg='pink', fg='white',
                               command=affiche_score)
            sub_quit = Button(fenetre, text="Quitter", font=("Cambria", 40), bg='pink', fg='white',
                              command=quitter_jeux)

            # Placement des widgets
            demineur.pack()
            jouer.pack(pady=10)
            sub_score.pack(pady=10)
            sub_quit.pack(pady=10)

        from tkinter import Tk

        ### Réglage fenêtre ###
        fenetre = Tk()
        fenetre.title("Démineur")
        fenetre['bg'] = 'grey'
        fenetre.attributes('-fullscreen', True)  # Plein écran activé

        ### Page Accueil ###
        demineur = Label(fenetre, text="Démineur", font=("Cambria", 75), bg='grey', fg='pink')
        jouer = Button(fenetre, text="Jouer", font=("Cambria", 40), bg='pink', fg='white', command=choix_difficulte)
        sub_score = Button(fenetre, text="Score", font=("Cambria", 40), bg='pink', fg='white', command=affiche_score)
        sub_quit = Button(fenetre, text="Quitter", font=("Cambria", 40), bg='pink', fg='white', command=quitter_jeux)

        # Affichage accueil
        demineur.pack()
        jouer.pack(pady=10)
        sub_score.pack(pady=10)
        sub_quit.pack(pady=10)

        fenetre.mainloop()



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
            messagebox.showinfo("Game Over", "You hit a mine! Game over.")
            self.root.destroy()
        elif self.game.is_won():
            messagebox.showinfo("Congratulations", "You won!")
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
