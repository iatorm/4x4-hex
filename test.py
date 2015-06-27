# This is a stupid example algorithm that can be used to test the controller.
# It does not implement a winning strategy.

import sys

# Input methods
STDIN = 0
ARGS  = 1
SPLIT = 2

INPUT = SPLIT

# Output formats
ZERO_BASED = 0
ONE_BASED  = 1
MODIFIED   = 2

OUTPUT = ZERO_BASED

# Player
WHITE = "W"
BLACK = "B"

PLAYER = WHITE

if INPUT == STDIN:
    board = input()
elif INPUT == ARGS:
    board = sys.argv[1]
else:
    board = "".join(sys.argv[1:])
response = board.index("E")
if OUTPUT == ZERO_BASED:
    print(response)
elif OUTPUT == ONE_BASED:
    print(response + 1)
else:
    print(board[:response] + PLAYER + board[response+1:])
