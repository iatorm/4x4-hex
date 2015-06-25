
from subprocess import check_output, Popen, PIPE

### Interaction

# Input types
STDIN    = 0
CMD_ARGS = 1
FUNCTION = 2 # uses player_strategy

# Change this to your liking
INPUT_TYPE = STDIN

# Output types
ZERO_BASED_INDEX = 0
ONE_BASED_INDEX  = 1
MODIFIED_BOARD   = 2

# Change this to your liking
OUTPUT_TYPE = ZERO_BASED_INDEX

# Change this to your liking; separate all arguments
COMMAND = ["python3", "test.py"]

# Player types
WHITE   = 0
BLACK   = 1
NEITHER = 2

# Change this to your liking
PLAYER = WHITE

def player_strategy(board):
    "For testing and wrapping solutions; returns a zero-based index"
    return board.index(NEITHER) # Example strategy

def enc_board(board):
    s = ""
    for v in board:
        if v == WHITE:
            s += "W"
        elif v == BLACK:
            s += "B"
        else:
            s += "E"
    return s

def dec_board(string):
    return [{"W":WHITE, "B":BLACK, "E":NEITHER}[c] for c in string]

class InputException(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

def strategy(command, in_type, out_type, player, function=None):
    def s(board):
        if in_type == FUNCTION:
            return player_strategy(board)
        else:
            message = enc_board(board)
            if in_type == STDIN:
                out = Popen(command, stdin=PIPE, stdout=PIPE, universal_newlines=True).communicate(message)[0].rstrip()
            elif in_type == CMD_ARGS:
                out = check_output(command + [message], universal_newlines=True).rstrip()
            if OUTPUT_TYPE == ZERO_BASED_INDEX:
                try:
                    out_num = int(out)
                    assert 0 <= out_num < 16 and message[out_num] == "E"
                    return out_num
                except:
                    raise InputException(message, out)
            elif OUTPUT_TYPE == ONE_BASED_INDEX:
                try:
                    out_num = int(out)
                    assert 1 <= out_num <= 16 and message[out_num] == "E"
                    return out_num
                except:
                    raise InputException(message, out)
            elif OUTPUT_TYPE == MODIFIED_BOARD:
                try:
                    assert len(out) == 16 and sum(1 for i in range(16) if out[i] != message[i]) == 1
                    diff = min(i for i in range(16) if out[i] != message[i])
                    assert message[diff] == "E" and out[diff] == ("W" if PLAYER == WHITE else "B")
                    return diff
                except:
                    raise InputException(message, out)
    return s


### Program logic

def enemy(player):
    if player == WHITE:
        return BLACK
    else:
        return WHITE

def nbors(i):
    "The set of neighbors of i in the board"
    if i > 3:
        yield i-4 # north
        if i%4 != 0:
            yield i-5 # northwest
    if i < 12:
        yield i+4 # south
        if i%4 != 3:
            yield i+5 # southeast
    if i%4 != 0:
        yield i-1 # west
    if i%4 != 3:
        yield i+1 # east

def win(board):
    "Is this position a win for either player?"
    seen = set()
    front = set(i for i in range(4) if board[i] == WHITE)
    while front:
        seen.update(front)
        front = set(j for i in front for j in nbors(i) if board[j] == WHITE and j not in seen)
    if any(i > 11 for i in seen):
        return WHITE
    seen = set()
    front = set(i*4 for i in range(4) if board[i] == BLACK)
    while front:
        seen.update(front)
        front = set(j for i in front for j in nbors(i) if board[j] == BLACK and j not in seen)
    if any(i%4 == 3 for i in seen):
        return BLACK
    return NEITHER

def winning(s, board, player):
    "Is s a winning strategy for the given player from the given position on their turn? Return also the losing game."
    winner = win(board)
    if winner == player:
        return (True, None)
    elif winner == enemy(player):
        return (False, [board])
    else:
        new = board[:]
        new[s(new)] = player
        for i in range(16):
            if new[i] == NEITHER:
                res, game = winning(s, new[:i] + [enemy(player)] + new[i+1:], player)
                if not res:
                    return (False, [board, new] + game)
        return (True, None)

### Main function

def main():
    if INPUT_TYPE != FUNCTION:
        s = strategy(COMMAND, INPUT_TYPE, OUTPUT_TYPE, PLAYER)
    else:
        s = strategy(player_strategy, INPUT_TYPE, OUTPUT_TYPE, PLAYER)
    try:
        res, game = winning(s, [NEITHER]*16, PLAYER)
        if res:
            print("This strategy is winning.")
        else:
            for board in game:
                for i in range(4):
                    print(enc_board(board)[4*i:4*(i+1)])
                print("----")
            print("This strategy is not winning.")
    except IOError as e:
        print("Something unexpected happened:\n", e)
    except InputException as e:
        print("Incorrect response '" + e.response + "' to message '" + e.message + "'.")

if __name__ == "__main__":
    main()
