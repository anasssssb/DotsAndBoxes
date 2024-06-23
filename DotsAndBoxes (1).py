# 21L-6297 Alishba Kamran
# 21L-5678 Anas Tanvir
# 21L7693 Usman Bin Imran


import tkinter as tk
from tkinter import messagebox, simpledialog
import copy
import math
import random
import time


class DotsAndBoxes:
    def __init__(self, rows, columns):
        self.play_dict = {}
        for i in range(rows):
            for j in range(columns - 1):
                self.play_dict[((j + i * columns), j + (i * columns) + 1)] = 0

        for i in range(rows - 1):
            for j in range(columns):
                self.play_dict[(j + (i * columns), j + columns + (i * columns))] = 0

        self.score_dict = {}
        for i in range(rows - 1):
            for j in range(columns - 1):
                box = [(j + i * columns, j + i * columns + 1)]
                box.append((box[0][0], box[0][1] + columns - 1))
                box.append((box[0][0] + 1, box[0][1] + columns))
                box.append((box[0][0] + columns, box[2][1]))
                self.score_dict[tuple(box)] = 0

        self.row_count = rows
        self.column_count = columns

        self.a_score = 0
        self.b_score = 0

    def make_row(self, i):
        left = (i * self.column_count)
        right = left + 1
        for j in range(self.column_count - 1):
            if self.play_dict[(left, right)] == 0:
                print("{:^3d}".format(left), end="   ")
            else:
                print("{:^3d} -".format(left), end=" ")
            left = right
            right = left + 1
        print("{:^3d}".format(left))

    def make_vertical(self, upper_left, upper_right):
        if self.play_dict[(upper_left, upper_right)] == 0:
            print("  ", end=" ")
        else:
            print(" |", end=" ")

    def make_middle_row(self, i):
        upper_left = (i * self.column_count)
        upper_right = upper_left + 1
        bottom_left = upper_left + self.column_count
        bottom_right = bottom_left + 1
        for j in range(self.column_count - 1):
            self.make_vertical(upper_left, bottom_left)

            top = (upper_left, upper_right)
            left = (upper_left, bottom_left)
            right = (upper_right, bottom_right)
            bottom = (bottom_left, bottom_right)
            score = self.score_dict[(top, left, right, bottom)]

            if score == 0:
                print("  ", end=" ")
            else:
                print(" " + score, end=" ")

            upper_left, bottom_left = upper_right, bottom_right
            upper_right += 1
            bottom_right += 1
        self.make_vertical(upper_left, bottom_left)
        print()

    def display_board(self):
        for i in range(self.row_count - 1):
            self.make_row(i)
            self.make_middle_row(i)

        self.make_row(self.row_count - 1)
        print("\nPlayer A: {} Player B: {}".format(self.a_score, self.b_score))

    def check_scores(self, player_a):
        player = "A" if player_a else "B"
        taken_set = {i for i in self.play_dict if self.play_dict[i] == 1}
        open_scores = [i for i in self.score_dict if self.score_dict[i] == 0]
        score_counter = 0
        for box in open_scores:
            if set(box).issubset(taken_set):
                score_counter += 1
                self.score_dict[box] = player
        return score_counter

    def make_play(self, start_point, end_point, player_a):
        try:
            if self.play_dict[(start_point, end_point)] == 1:
                return False
        except KeyError:
            return False

        self.play_dict[(start_point, end_point)] = 1
        score = self.check_scores(player_a)
        if player_a:
            self.a_score += score
        else:
            self.b_score += score
        return True

    def get_available_plays(self):
        return [i for i in self.play_dict if self.play_dict[i] == 0]

    def is_game_over(self):
        return self.a_score + self.b_score == len(self.score_dict)


class MinimaxPlayer:
    def __init__(self, player_a):
        self.player = player_a

    def minimax(self, game, play, depth, alpha, beta, player_a):
        if game.is_game_over() or depth == 0:
            return (game.a_score - game.b_score, play)
        if player_a:
            value = -math.inf
            for move in game.get_available_plays():
                new_game = copy.deepcopy(game)
                old_score = new_game.a_score
                new_game.make_play(*move, True)
                new_score = new_game.a_score
                if new_score == old_score:
                    new_play_results = self.minimax(new_game, move, depth - 1, alpha, beta, False)
                else:
                    new_play_results = self.minimax(new_game, move, depth - 1, alpha, beta, True)
                if value >= new_play_results[0]:
                    play = move
                    value = new_play_results[0]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (value, play)
        else:
            value = math.inf
            for move in game.get_available_plays():
                new_game = copy.deepcopy(game)
                old_score = new_game.b_score
                new_game.make_play(*move, False)
                new_score = new_game.b_score
                if new_score == old_score:
                    move_results = self.minimax(new_game, move, depth - 1, alpha, beta, True)
                else:
                    move_results = self.minimax(new_game, move, depth - 1, alpha, beta, False)
                if value <= move_results[0]:
                    play = move
                    value = move_results[0]
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return (value, play)

    def make_play(self, game):
        start_time = time.time()
        play_space_size = len(game.get_available_plays())
        if play_space_size == 1:
            play = random.choice(game.get_available_plays())
            game.make_play(*play, self.player)
            return
        depth = math.floor(math.log(19000, play_space_size))
        play = self.minimax(game, (0, 0), depth, -math.inf, math.inf, self.player)[1]
        elapsed = time.time() - start_time

        if play == (0, 0):
            play = random.choice(game.get_available_plays())
        game.make_play(*play, self.player)

        player = "A" if self.player else "B"
        print("Player {}'s move: {} {}".format(player, *play))


class HumanPlayer:
    def __init__(self, player_a):
        self.player_a = player_a
        self.playername = "A" if player_a else "B"

    def make_play(self, game):
        while True:
            move = input(f"Player {self.playername}, make your move (start_point end_point): ")
            move = move.split()
            move[0], move[1] = int(move[0]), int(move[1])
            move.sort()
            valid_move = game.make_play(*move, self.player_a)
            if valid_move:
                break


class Game:
    def __init__(self, player_a_type="human", player_b_type="minimax", rows=5, columns=5):
        self.rows = rows
        self.columns = columns

        if player_a_type == "human":
            self.player_a = HumanPlayer(True)
        elif player_a_type == "minimax":
            self.player_a = MinimaxPlayer(True)

        if player_b_type == "human":
            self.player_b = HumanPlayer(False)
        elif player_b_type == "minimax":
            self.player_b = MinimaxPlayer(False)

    def play_game(self):
        game_instance = DotsAndBoxes(self.rows, self.columns)
        print()
        game_instance.display_board()
        print()
        while not game_instance.is_game_over():
            self.player_a.make_play(game_instance)
            game_instance.display_board()
            if not game_instance.is_game_over():
                self.player_b.make_play(game_instance)
                game_instance.display_board()

        if game_instance.a_score == game_instance.b_score:
            print("It's a tie!")
        elif game_instance.a_score > game_instance.b_score:
            print("Player A wins!")
        else:
            print("Player B wins!")


class WelcomeScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Dots And Boxes")
        self.root.geometry("400x200")

        label = tk.Label(self.root, text="Welcome to Dots And Boxes", font=("Helvetica", 20))
        label.pack(pady=20)

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.pack()

        self.root.mainloop()

    def start_game(self):
        self.root.destroy()  # Close the welcome screen
        self.configure_game()

    def configure_game(self):
        player_a_type = self.prompt_player_type("Player A")
        player_b_type = self.prompt_player_type("Player B")
        rows = self.prompt_grid_size("rows")
        columns = self.prompt_grid_size("columns")
        gameplay = Game(player_a_type, player_b_type, rows, columns)
        gameplay.play_game()

    def prompt_player_type(self, player_name):
        player_type = simpledialog.askstring("Player Type", f"Choose {player_name} type ('human' or 'minimax'): ").lower()
        while player_type not in ['human', 'minimax']:
            player_type = simpledialog.askstring("Player Type", f"Invalid input. Choose {player_name} type ('human' or 'minimax'): ").lower()
        return player_type

    def prompt_grid_size(self, dimension):
        size = simpledialog.askinteger("Grid Size", f"How many {dimension} should the grid have? ")
        while size is None or size <= 0:
            size = simpledialog.askinteger("Grid Size", f"Invalid input. Please enter a positive integer for {dimension}: ")
        return size


def main():
    WelcomeScreen()


if __name__ == "__main__":
    main()
