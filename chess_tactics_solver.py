import chess
import numpy as np

piece_dict = { # Maps pieces to their values
'P':1,   # White pawn
'R':5,   # White rook
'N':3,   # White knight
'B':3,   # White bishop
'Q':9,   # White queen
'K':100, # White king
'.':0,   # Empty square
'p':-1,  # Black pawn
'r':-5,  # Black rook
'n':-3,  # Black knight
'b':-3,  # Black bishop
'q':-9,  # Black queen
'k':-100,# Black king
' ':0,   # Aesthetic buffer value in string translation
'\n':0,  # Similar to ^
}
position_table = {}


def mate_in_one(position):
    '''
    Accepts a given chess position where there is potentially a mate in one
    somewhere, and returns the move that delivers checkmate.  If no legal 
    move will deliver checkmate, then the None value is returned.
    '''
    correct_move = None
    # Iterate through all legal moves
    for move in position.legal_moves:
        # Make the move, and check to see if the position is checkmate
        position.push(move)
        if position.is_checkmate():
            # if it is, then set the correct move, undo the last move so
            # that the original position is present, and break out of the
            # loop.
            correct_move = move
            position.pop()
            break
        else:
            position.pop() # pop the last move if it's not checkmate.
    return correct_move

def mate_in_two(position):
    '''
    Accepts a chess position where there is potentially a mate in two
    somewhere, and returns the move that leads to checkmate.  If there is
    no such move, then None value is returned.
    '''
    correct_move = None
    for move1 in position.legal_moves:
        position.push(move1)
        broke = False # flag: becomes true if mate can be avoided
        for move2 in position.legal_moves:
            position.push(move2)
            if mate_in_one(position) is None:
                # If we reach a position where mate is avoided, then set
                # the broke flag to True, and try a new move1
                broke = True
                position.pop()
                break
            else:
                position.pop()
        if not broke:
            correct_move = move1
            position.pop()
            break
        else:
            position.pop()
    return correct_move

def simple_evaluate(position):
    '''
    Determines the value of the position by comparing piece value and
    nothing more.  A higher evaluation value translates to a higher
    advantage for white.
    '''
    boardfen = position.fen()


    if boardfen in position_table:
        return position_table[boardfen]

    r = position.result()
    if r == '1-0':
        return 9999 # White has won
    elif r == '0-1':
        return -9999 # Black has won
    elif r == '1/2-1/2':
        return 0 # Draw, regardless of piece value (to avoid stalemates)
    board_val = 0
    for c in str(position):
        board_val += piece_dict[c]
    return board_val

#returns the next state
def MiniMaxAB(board, depth=3):
    count = 0
    if board.turn:
        v = MaxValue(board,-np.inf,np.inf,depth,count)
    else:
        v = MinValue(board,-np.inf,np.inf,depth,count)
    for x in board.legal_moves:
        board.push(x)
        if simple_evaluate(board) == v:
            board.pop()
            return x
        else:
            board.pop()


def MaxValue(state,a,b,depth,count):
    if count == 3:
        return simple_evaluate(state)
    if simple_evaluate(state) == 9999 or simple_evaluate(state) == -9999 or simple_evaluate(state) == 0:
        return simple_evaluate(state)
    v = -np.inf
    for x in state.legal_moves:
        state.push(x)
        v = max(v,MinValue(state,a,b,depth,count))
        state.pop()
        if v >= b:
            return v
        a = max(a,v)
    return v

def MinValue(state,a,b,depth,count):
    if count == 3:
        return simple_evaluate(state)
    if simple_evaluate(state) == 9999 or simple_evaluate(state) == -9999 or simple_evaluate(state) == 0:
        return simple_evaluate(state)
    v = np.inf
    for x in state.legal_moves:
        state.push(x)
        v = min(v,MaxValue(state,a,b,depth,count))
        state.pop()
        if v <= a:
            return v
        b = min(b,v)
    return v

def main():
    board = chess.Board("8/8/6Rp/1ppPk3/p3Pp2/2P1nP2/P6P/2K5 w - - 2 46")
    init = board.turn
    while(not(simple_evaluate(board) == 9999 or simple_evaluate(board) == -9999 or simple_evaluate(board) == 0)):
        x = MiniMaxAB(board)
        board.push(board.push(x))

main()
    
