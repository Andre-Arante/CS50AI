from numpy import true_divide


def vertical_check(board, player):
    return (all(element == player for (_, _, element) in board)) or (all(element == player for (_, element, _) in board)) or (all(element == player for (element, _, _) in board)) 

def horizontal_check(board, player):
    for i, e in enumerate(board):
        if (all(element == player for element in e)):
             return True

    return False

def diagonal_check(board, player):
    corners = [[0, 0, 1], [2, 0, -1]]

    for corner in corners:
        diagonal = []
        for _ in range(3):
            diagonal.append(board[corner[0]][corner[1]])
            corner[0], corner[1] = corner[0]+corner[2], corner[1]+1
        if (all(element == player for element in diagonal)):
            return True
    return False

def all_spots_filled(board):
    for i, e in enumerate(board):
        for j, e in enumerate(board[i]):
            if board[i][j] is None:
                return False
    return True


