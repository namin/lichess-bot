import chess
import random
from chess_strategies import alpha_zero_strategy

def random_strategy(board):
    move = random.choice(list(board.legal_moves))
    return move.uci()

# Add your strategies to this dictionary.
# Key: name
# Value: function from chess.Board to chess.Move
strategies = {'random':random_strategy, 'alpha-zero':alpha_zero_strategy}
