"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
rows_n_cols = 3
moovex = []
mooveo = []

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
    if action == None:
        return board
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
    if winner(board):
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
    if terminal(board):
        return None
    
    # if board == initial_state():
    #     return (2,2)
     
    # X try to maximize, O tries to minimize
    who_play = player(board)
    move_current = None

    if who_play == O:
        v_current = 99
        for move in actions(board):

            # Resulting board, after this move
            current_board = result(board, move)

            # I made the move, then calculate the futures moves 
            v = max_value(current_board)

            # Prunnig
            if v == -1:
                return move
            elif v_current > v:
                v_current = v
                move_current = move
        return move_current
    
    else:
        v_current = -99
        for move in actions(board):
            current_board = result(board, move)
            v = min_value(current_board)

            if v == 1:
                return move
            elif v_current < v:
                v_current = v
                move_current = move
        return move_current


def min_value(board):
    v = 99      # Best minimum value
    if terminal(board):
        return utility(board)
    for move in actions(board):
        v= min(v, max_value(result(board, move)))
        # Alpha-Beta prunning: If I found the min value, is not necesarry find anymore
        if v == -1:
            return v
    return v
    
def max_value(board):
    v = -99     # Best maximun value
    if terminal(board):
        return utility(board)
    for move in actions(board):
        v = max(v, min_value(result(board, move)))
        # Alpha-Beta prunning: If I found the max value, is not necesarry find anymore
        if v == 1:
            return v
    return v