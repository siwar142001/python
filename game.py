import random
import tkinter as tk
from tkinter import messagebox

class Minesweeper:
    def __init__(self, rows, columns, bombs):
        self.__rows = rows
        self.__columns = columns
        self.__bombs = bombs
        self.__matrix = [["0" for _ in range(columns)] for _ in range(rows)]
        self.__display_matrix = [[" " for _ in range(columns)] for _ in range(rows)]
        self.__flags = 0
        self.__first_click = True

    def __place_bombs(self, first_click_row, first_click_col):
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            i = random.randint(0, self.__rows - 1)
            j = random.randint(0, self.__columns - 1)
            if (i, j) != (first_click_row, first_click_col) and self.__matrix[i][j] != "B":
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

    def click_cell(self, row, col):
        if self.__first_click:
            self.__place_bombs(row, col)
            self.__calculate_numbers()
            self.__first_click = False

        if self.__matrix[row][col] == "B":
            return "lost"

        self.__reveal_cells(row, col)
        return "continue"

    def toggle_flag(self, row, col):
        if self.__display_matrix[row][col] == " ":
            self.__display_matrix[row][col] = "F"
            self.__flags += 1
        elif self.__display_matrix[row][col] == "F":
            self.__display_matrix[row][col] = " "
            self.__flags -= 1

    def is_won(self):
        revealed_cells = sum(row.count(" ") for row in self.__display_matrix)
        return revealed_cells == self.__bombs

    def get_display_matrix(self):
        return self.__display_matrix

class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.game = Minesweeper(9, 9, 10)  # Default to easy mode
        self.buttons = []

        self.__create_widgets()

    def __create_widgets(self):
        for i in range(9):
            row_buttons = []
            for j in range(9):
                btn = tk.Button(self.root, text=" ", width=3, height=1, command=lambda r=i, c=j: self.__on_click(r, c))
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.__on_right_click(r, c))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def __on_click(self, row, col):
        result = self.game.click_cell(row, col)
        self.__update_buttons()

        if result == "lost":
            messagebox.showinfo("Game Over", "You hit a mine! Game over.")
            self.root.destroy()
        elif self.game.is_won():
            messagebox.showinfo("Congratulations", "You won!")
            self.root.destroy()

    def __on_right_click(self, row, col):
        self.game.toggle_flag(row, col)
        self.__update_buttons()

    def __update_buttons(self):
        display_matrix = self.game.get_display_matrix()
        for i in range(9):
            for j in range(9):
                self.buttons[i][j].config(text=display_matrix[i][j])

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
