import tkinter as tk
from tkinter import messagebox, simpledialog
import time
from game_logic import Minesweeper
from score_manager import ScoreManager


class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.score_manager = ScoreManager()  # Gestionnaire des scores
        self.difficulty = None
        self.player_name = "Joueur"
        self.game = None

        self.buttons = []
        self.start_time = None
        self.is_game_over = False
        self.__create_home_menu()

    def __create_home_menu(self):
        """Crée le menu d'accueil principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        tk.Label(self.root, text="Bienvenue sur Minesweeper !", font=("Arial", 30)).pack(pady=20)
        tk.Button(self.root, text="Commencer le jeu", font=("Arial", 20),
                  command=self.__create_difficulty_menu).pack(pady=10)
        tk.Button(self.root, text="Hall of Fame", font=("Arial", 20),
                  command=self.__show_hall_of_fame).pack(pady=10)
        tk.Button(self.root, text="Quitter", font=("Arial", 20), command=self.root.quit).pack(pady=10)

    def __create_difficulty_menu(self):
        """Affiche un menu pour choisir la difficulté."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choisissez une difficulté", font=("Arial", 30)).pack(pady=20)
        tk.Button(self.root, text="Facile (9x9, 10 bombes)", font=("Arial", 20),
                  command=lambda: self.__ask_player_name_and_start_game(9, 9, 10, "Facile")).pack(pady=10)
        tk.Button(self.root, text="Moyen (16x16, 40 bombes)", font=("Arial", 20),
                  command=lambda: self.__ask_player_name_and_start_game(16, 16, 40, "Moyen")).pack(pady=10)
        tk.Button(self.root, text="Difficile (30x16, 99 bombes)", font=("Arial", 20),
                  command=lambda: self.__ask_player_name_and_start_game(30, 16, 99, "Difficile")).pack(pady=10)
        tk.Button(self.root, text="Retour", font=("Arial", 20), command=self.__create_home_menu).pack(pady=10)

    def __ask_player_name_and_start_game(self, rows, cols, bombs, difficulty):
        player_name = simpledialog.askstring("Nom du joueur", "Entrez votre nom :", parent=self.root)
        self.player_name = player_name.strip() if player_name else "Joueur"
        self.__start_game(rows, cols, bombs, difficulty)

    def __start_game(self, rows, columns, bombs, difficulty):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.difficulty = difficulty
        self.game = Minesweeper(rows, columns, bombs)
        self.buttons = []
        self.start_time = time.time()
        self.is_game_over = False

        # Frame pour centrer le jeu
        game_frame = tk.Frame(self.root)
        game_frame.pack(expand=True)

        # Ajouter le label du chrono
        self.timer_label = tk.Label(game_frame, text="Temps: 0 secondes", font=("Arial", 20), bg="#AED6F1",
                                    fg="#34495E")
        self.timer_label.grid(row=0, column=0, columnspan=columns, pady=(0, 10))

        # Configurer la grille pour s'ajuster à la taille de la fenêtre
        game_frame.grid_columnconfigure(0, weight=1)
        game_frame.grid_rowconfigure(0, weight=1)

        for i in range(rows):
            row_buttons = []
            game_frame.grid_rowconfigure(i + 1, weight=1)  # Chaque ligne peut se redimensionner

            for j in range(columns):
                btn = tk.Button(game_frame, text=" ", width=3, height=1)
                btn.grid(row=i + 1, column=j,
                         sticky="news")  # Utilisation de sticky pour faire en sorte que les boutons s'ajustent
                btn.bind("<Button-1>", lambda e, r=i, c=j: self.__on_click(r, c))
                btn.bind("<Button-2>", lambda e, r=i, c=j: self.__on_right_click(r, c))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.__update_timer()

    def __update_timer(self):
        if self.is_game_over:
            return

        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Temps: {elapsed_time} secondes")
        self.root.after(1000, self.__update_timer)

    def __on_click(self, row, col):
        result = self.game.click_cell(row, col)
        self.__update_buttons()

        if result == "lost":
            self.is_game_over = True
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Game Over", f"Vous avez perdu en {elapsed_time} secondes!")
            self.__save_score(elapsed_time, won=False)

            self.endgame_menu()

        elif self.game.is_won():
            self.is_game_over = True
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Félicitations", f"Vous avez gagné en {elapsed_time} secondes!")
            self.__save_score(elapsed_time, won=True)

            self.endgame_menu()

    def __on_right_click(self, row, col):
        self.game.toggle_flag(row, col)
        self.__update_buttons()

    def __update_buttons(self):
        display_matrix = self.game.get_display_matrix()
        for i, row in enumerate(display_matrix):
            for j, value in enumerate(row):
                self.buttons[i][j].config(text=value)

    def endgame_menu(self):
        """
        Affiche un menu à la fin de la partie avec un message et des options.
        """
        # Crée une nouvelle fenêtre pour la fin de la partie
        endgame_window = tk.Toplevel(self.root)
        endgame_window.title("Fin de partie")
        endgame_window.geometry("400x300")
        endgame_window.configure(bg="#AED6F1")

        # Message de victoire ou défaite
        if self.game.is_won():
            message = "Félicitations, vous avez gagné !"
        else:
            message = "Dommage, vous avez perdu."

        # Label pour le message
        tk.Label(
            endgame_window,
            text=message,
            font=("Arial", 16),
            bg="#AED6F1",
            fg="#34495E",
            wraplength=300,
            justify="center"
        ).pack(pady=20)

        # Crée un grand bouton pour "Nouvelle Partie"
        tk.Button(
            endgame_window,
            text="Nouvelle Partie",
            font=("Arial", 20),
            bg="#3498DB",
            fg="white",
            command=self.__create_home_menu  # Retour au menu principal
        ).pack(pady=20)

        # Ajoute un Frame pour organiser les deux boutons plus petits
        button_frame = tk.Frame(endgame_window, bg="#AED6F1")
        button_frame.pack(pady=10)

        # Bouton "Recommencer"
        tk.Button(
            button_frame,
            text="Recommencer",
            font=("Arial", 14),
            bg="#FADBD8",
            fg="#34495E",
        ).grid(row=0, column=0, padx=10)

        # Bouton "Enregistrer"
        tk.Button(
            button_frame,
            text="Enregistrer",
            font=("Arial", 14),
            bg="#FADBD8",
            fg="#34495E",
        ).grid(row=0, column=1, padx=10)

    def __save_score(self, elapsed_time, won):
        grid_id = f"{self.difficulty}_grid"
        if won:
            self.score_manager.add_score(self.player_name, elapsed_time, self.difficulty, grid_id)

    def __show_hall_of_fame(self):
        hall_of_fame = self.score_manager.get_hall_of_fame(self.difficulty)
        if not hall_of_fame:
            messagebox.showinfo("Hall of Fame", "Aucun score enregistré.")
            return

        score_message = "\n".join(f"{score['player_name']} - {score['elapsed_time']} secondes" for score in hall_of_fame)
        messagebox.showinfo("Hall of Fame", f"--- Hall of Fame ---\n{score_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
