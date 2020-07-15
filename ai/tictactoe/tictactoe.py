"""
Tic Tac Toe Player
"""
import copy
import math

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
    x_count, o_count = 0, 0

    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                x_count += 1
            if board[row][col] == "O":
                o_count += 1

    if x_count == o_count:
        return "X"
    return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.append([i, j])
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    boardcopy = copy.deepcopy(board)

    if board[action[0]][action[1]] != None:
        raise IndexError

    boardcopy[action[0]][action[1]] = player(boardcopy)
    return boardcopy





def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        x_count = row.count(X)
        o_count = row.count(O)

        if x_count == 3:
            return X
        if o_count == 3:
            return O

        
                

    for i in range(3):
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        if board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O

    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    
    count = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] != None:
                count += 1

    if count == 9:
        return True
    
    return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    if player(board) == X:
        v = -math.inf

        for action in actions(board):
            move = minval(result(board,action),-2,2)
            if move > v:
                v = move
                best_move = action

    else:
        v = math.inf

        for action in actions(board):
            move = maxval(result(board,action),-2,2)
            if move < v:
                v = move
                best_move = action
    return best_move

def maxval(board,alpha,beta):
    if terminal(board):
        return utility(board)

    v = -2
    for action in actions(board):
        v = max(v,minval(result(board,action),alpha,beta))
        alpha = max(alpha, v)
        if alpha > beta:
            break
    return v

def minval(board,alpha,beta):
    if terminal(board):
        return utility(board)

    v = 2
    for action in actions(board):
        v = min(v,maxval(result(board,action),alpha,beta))
        beta = min(v, beta)
        if alpha > beta:
            break
    return v