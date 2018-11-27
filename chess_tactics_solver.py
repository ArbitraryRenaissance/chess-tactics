import chess

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
