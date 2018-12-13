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
    global position_table
    boardfen = position.fen()
    if boardfen in position_table:
        return position_table[boardfen]

    r = position.result()
    if r == '1-0':
        #position_table[boardfen] = 9999
        return 9999 # White has won
    elif r == '0-1':
        #position_table[boardfen] = -9999
        return -9999 # Black has won
    elif r == '1/2-1/2':
        #position_table[boardfen] = 0
        return 0 # Draw, regardless of piece value (to avoid stalemates)
    board_val = 0
    for c in str(position):
        board_val += piece_dict[c]
    #position_table[boardfen] = board_val
    return board_val

#returns the next state
def MiniMaxAB(board,depth):
    global position_table
    v = AlphaBetaIterative(board,depth,-np.inf,np.inf)
    for x in board.legal_moves:
        board.push(x)
        if (board.fen() in position_table and
        position_table[board.fen()]==v):
            board.pop()
            return x
        else:
            board.pop()

def MaxValue(state,a,b,depth,count):
    global position_table
    if count == depth:
        # We've reached the end
        return simple_evaluate(state)
    if state.fen() in position_table:
        # We've been here before
        return position_table[state.fen()]
    if state.is_checkmate():
        # We be mated
        return simple_evaluate(state)
    v = -np.inf
    searchDomain = state.legal_moves
    for x in searchDomain:
        state.push(x)
        v = max(v,MinValue(state,a,b,depth,count+0.5))
        state.pop()
        if v >= b:
            position_table[state.fen()] = v
            return v
        a = max(a,v)
    position_table[state.fen()] = v
    return v

def MinValue(state,a,b,depth,count):
    global position_table
    if count == depth:
        # We've reached the end
        v = simple_evaluate(state)
        position_table[state.fen()] = v
        return v
    if state.fen() in position_table:
        # We've been here before
        return position_table[state.fen()]
    if state.is_checkmate():
        # We be mated
        return simple_evaluate(state)
    v = np.inf
    searchDomain = state.legal_moves
    for x in searchDomain:
        state.push(x)
        v = min(v,MaxValue(state,a,b,depth,count+0.5))
        state.pop()
        if v <= a:
            position_table[state.fen()] = v
            return v
        b = min(b,v)
    return v

def AlphaBetaIterative(position, depth, a, b):
    global position_table
    if position.fen() in position_table:
        return position_table[position.fen()]
    '''
    if a >= 3:
        # White is definitely better: tactic found or blunder made
        position_table[position.fen()] = a
        return a
    elif b <= -3:
        # Black is definitely better
        position_table[position.fen()] = b
        return b
    '''
    maximizingPlayer = position.turn
    if depth == 0 or position.is_checkmate():
        return simple_evaluate(position)
    if maximizingPlayer:
        v = -np.inf
        for m in position.legal_moves:
            pcopy = position.copy()
            pcopy.push(m)
            v = max(v, AlphaBetaIterative(pcopy,depth-0.5,a,b))
            if v >= b:
                break # b cut-off
            a = max(a,v)
        position_table[position.fen()] = v
        return v
    else:
        v = np.inf
        for m in position.legal_moves:
            pcopy = position.copy()
            pcopy.push(m)
            v = min(v, AlphaBetaIterative(pcopy,depth-0.5,a,b))
            if v <= a:
                break # a cut-off
            b = min(b,v)
        position_table[position.fen()] = v
        return v


def Solve(position):
    move = mate_in_two(position)
    if not move is None:
        return move
    else:
        move = MiniMaxAB(position,2)
    position.push(move)
    if position_table[position.fen()] in [-1,0,1]:
        print("Probably not the ideal move here, by the way ... ")
    position.pop()
    return move

def main():
    board = chess.Board("8/8/6Rp/1ppPk3/p3Pp2/2P1nP2/P6P/2K5 w - - 2 46")
    init = board.turn
    while(not(simple_evaluate(board) == 9999 or simple_evaluate(board) == -9999 or simple_evaluate(board) == 0)):
        x = MiniMaxAB(board)
        board.push(board.push(x))

# FENS that work:
# 8/7p/5Bp1/P4p2/q1p1rNk1/6P1/5P1P/5RK1 w - - 1 35 (mate)
# r7/5ppp/2k5/1p6/1Kp1b1P1/P1B4P/1P3P1R/4RB2 b - - 5 33 (mate)
# 1r1r2k1/p4p1p/3b2p1/1p1Q4/2p1B3/4P3/q1PP2PP/1N3RK1 w - - 2 21 (luck?)
# r1b3k1/1p3pp1/p7/3NP2r/8/P3K1RP/1P3p2/5R2 w - - 0 31 (tactic)
# 3r4/5pk1/p3p1p1/1p1bPq2/3R1P2/8/PP4P1/2QB2K1 w - - 1 30 (tactic, takes t)
