"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
rows_n_cols = 3

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    nones_qtty = sum(row.count(None) for row in board)
    if nones_qtty % 2 == 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == None:
                moves.add((i, j))
    if not moves:
        return {(0,0)}
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # board is an array, action is a tuple 
    copy_board = deepcopy(board)
    rows_n_cols = len(copy_board)

    if action[0]<rows_n_cols and action[1]<rows_n_cols and copy_board[action[0]][action[1]] is None:
        who_play = player(copy_board)
        copy_board[action[0]][action[1]] = who_play
        return copy_board
    raise ValueError("Invalid movement.")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(rows_n_cols):
        # ROWS: winner by row. So the first can't be None
        if board[i][0] != None:
            if all(cell == board[i][0] for cell in board[i]):   # Each row element, must be equal to the first element in the row
                return board[i][0]
            
        # COLS: winner by col. So the first can't be None
        if board[0][i] != None:
            if all(row[i] == board[0][i] for row in board):     # Within each row, compare element i with the first element of the i column
                return board[0][i]

    dg_l2r = 0  # Diagonal left to right
    dg_r2l = 0  # Diagonal right to left

    for i in range(rows_n_cols):
        if board[i][i] == board[0][0]:
            dg_l2r += 1 
        if board[i][rows_n_cols - 1 - i] == board[0][-1]:
            dg_r2l += 1
    
    if dg_l2r == rows_n_cols:
        return board[0][0]
    elif dg_r2l == rows_n_cols:
        return board[0][-1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    # If I found None, then Any=True, but I need false beacuse None moves still exists. So, I use not().
    return not(any(None in row for row in board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None
    
    available_moves = actions(board)

    for move in available_moves:
        v = min(v, result(board, move))

    return (0,0)
