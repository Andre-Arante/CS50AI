"""
Tic Tac Toe Player
"""

import math
import copy

from util import vertical_check, horizontal_check, diagonal_check, all_spots_filled

from matplotlib.axis import XAxis

X = "X"
O = "O"
EMPTY = None



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
    num_x, num_o = 0, 0

    for i, e in enumerate(board):
        for j, e in enumerate(board[i]):
            if board[i][j] == X:
                num_x+=1
            elif board[i][j] == O:
                num_o+=1
    
    return O if (num_x > num_o) else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for i, e in enumerate(board):
        for j, e in enumerate(board[i]):
            if board[i][j] == EMPTY:
                actions.append([i, j])
    
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if vertical_check(board, X) or horizontal_check(board, X) or diagonal_check(board, X):
        return X
    elif vertical_check(board, O) or horizontal_check(board, O) or diagonal_check(board, O):
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or all_spots_filled(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    return -1 if w == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move


def min_value(board):
    if terminal(board): 
        return utility(board), None

    else:
        v = 999
        best_action = None

        for action in actions(board):
            value, move = max_value(result(board, action))

            if value < v:
                v = value
                best_action = action
                if v == -1:
                    return v, best_action
        return v, best_action

def max_value(board):
    if terminal(board): 
        return utility(board), None

    else:
        v = -999
        best_action = None

        for action in actions(board):
            value, move = min_value(result(board, action))

            if value > v:
                v = value
                best_action = action
                if v == 1:
                    return v, best_action
        return v, best_action

print(minimax([[EMPTY, X, O],
            [O, X, X],
            [X, EMPTY, O]]))


    
