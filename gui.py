import tkinter as tk
from tkinter import messagebox
import time
import pygame
from game_logic import Minesweeper

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
        self.start_time = None  # Début du chronomètre
        self.is_game_over = False  # Indicateur de fin de jeu
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

        tk.Button(home_frame, text="Commencer le jeu", font=("Arial", 50),bg='#3498DB',fg='#4a4e69', command=self.__create_difficulty_menu).pack(pady=15)

        tk.Button(home_frame, text="Quitter", font=("Arial", 30),bg='#E74C3C',fg='#4a4e69', command=self.root.quit).pack(pady=50)

        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
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
        self.start_time = time.time()  # Démarre le chronomètre
        self.is_game_over = False  # Réinitialise l'indicateur

        # Label pour afficher le chronomètre
        self.timer_label = tk.Label(self.root, text="Temps: 0 secondes", font=("Arial", 20), bg="#AED6F1", fg="#34495E")
        self.timer_label.grid(row=0, column=0, columnspan=columns, pady=(0, 10))

        # Configure la grille de boutons
        for i in range(rows):
            row_buttons = []
            for j in range(columns):
                btn = tk.Button(self.root, text=" ", width=3, height=1)
                btn.grid(row=i + 1, column=j)  # Décalage d'une ligne à cause du label

                # Gestion des clics gauche et droit
                btn.bind("<Button-1>", lambda e, r=i, c=j: self.__on_click(e, r, c))
                btn.bind("<Button-2>", lambda e, r=i, c=j: self.__on_right_click(e, r, c))

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Lancer la mise à jour du chronomètre
        self.__update_timer()

    def __update_timer(self):
        """
        Met à jour le chronomètre toutes les secondes.
        Affiche le temps sur l'interface.
        :return: Fin de la partie pour déclencher la fin du chronomètre
        """
        if self.is_game_over:
            return  # Arrête la mise à jour si la partie est terminée

        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Temps: {elapsed_time} secondes")  # Met à jour le texte du label
        # print(elapsed_time) # Solution du chronomètre
        # Appelle cette méthode toutes les secondes
        self.root.after(1000, self.__update_timer)

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
            self.is_game_over = True  # Arrête le chronomètre
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Game Over", f"Vous avez perdu en {elapsed_time} secondes!")
            pygame.mixer.quit()
            self.root.destroy()
        elif self.game.is_won():
            self.is_game_over = True  # Arrête le chronomètre
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Félicitations", f"Vous avez gagné en {elapsed_time} secondes!")
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