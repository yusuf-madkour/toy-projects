from random import choice
from colorama import Fore, init
from os import system
import platform
from time import sleep

maps = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), '9': (2, 2)}


def new_board():
    return [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]


def get_lines(board):
    return [
        board[0], board[1], board[2],             # All rows
        [board[0][0], board[1][0], board[2][0]],  # First column
        [board[0][1], board[1][1], board[2][1]],  # Second column
        [board[0][2], board[1][2], board[2][2]],  # Third column
        [board[0][0], board[1][1], board[2][2]],  # First diagonal
        [board[0][2], board[1][1], board[2][0]]   # Second diagonal
    ]


def render(board):
    system('clear') if platform.system() == 'Linux' else system('cls')
    print(cyan + '+-----+')
    for row in board:
        print(cyan + '|', end='')
        for i, c in enumerate(row):
            if c == 'X':
                print(red + 'X', end='')
            elif c == 'O':
                print(green + 'O', end='')
            else:
                print(c, end='')
            if i != 2:
                print(' ', end="")
        print(cyan + '|')
    print(cyan + '+-----+')


def human_player(board, player):
    print(f"Player {player}, what is your move?")
    n = input()
    while n not in maps:
        render(board)
        print("Input must be a number between 1 and 9, please try again.")
        print(f"Player {player}, what is your move?")
        n = input()
    return maps[n]


def finds_winning_and_losing_moves_ai(board, player):
    lines = get_lines(board)
    enemy = 'X' if player == 'O' else 'O'
    for line in lines:
        if line.count(player) == 2 and line.count(enemy) == 0:
            [winning_move] = [i for i in line if i != player]
            return maps[winning_move]
    for line in lines:
        if line.count(enemy) == 2 and line.count(player) == 0:
            [blocking_move] = [i for i in line if i != enemy]
            return maps[blocking_move]
    return random_ai(board, player)


def finds_winning_moves_ai(board, player):
    lines = get_lines(board)
    for line in lines:
        if line.count(player) == 2 and any(i.isnumeric() for i in line):
            [winning_move] = [i for i in line if i.isnumeric()]
            return maps[winning_move]
    return random_ai(board, player)


def random_ai(board, player):
    legal = [i for row in board for i in row if i not in ["X", "O"]]
    return maps[choice(legal)]


def make_move(board, coord, player):
    while board[coord[0]][coord[1]] in ['X', 'O']:
        render(board)
        print('Cell already full, please try again.')
        coord = human_player(board, player)
    board[coord[0]][coord[1]] = player
    return board


def full_board(board):
    return all([i in ['X', 'O'] for row in board for i in row])


def get_winner(board):
    lines = get_lines(board)
    for line in lines:
        if all(i == 'X' for i in line):
            return 'X'
        if all(i == 'O' for i in line):
            return 'O'
    return None


if __name__ == "__main__":
    init(autoreset=True)  # Initializing Colorama

    # Colorama colors used in rendering the board
    cyan = Fore.CYAN
    red = Fore.RED
    green = Fore.GREEN

    player = choice(['O', 'X'])  # Randomly choose who plays first
    board = new_board()
    while True:
        render(board)
        coords = human_player(board, player)
        board = make_move(board, coords, player)
        if get_winner(board):
            render(board)
            print(f"Player {get_winner(board)} wins", end='')
            break
        if full_board(board):
            render(board)
            print('Draw!!', end='')
            break
        player = 'O' if player == 'X' else 'X'
