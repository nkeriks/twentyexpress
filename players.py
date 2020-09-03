import game
import numpy as np

"""
Players take a draw (list of 20 elements) and return their filled in board.
"""


def random_player(draw):
    pos = np.arange(len(draw))
    np.random.shuffle(pos)
    return draw[pos]


def sequential_player(draw):
    pos = np.arange(len(draw))
    return draw[pos]


# ugh
closest_positions = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 4,
    10: 4,
    11: 5,
    12: 6,
    13: 7,
    14: 8,
    15: 9,
    16: 10,
    17: 11,
    18: 12,
    19: 13,
    20: 14,
    21: 14,
    22: 15,
    23: 15,
    24: 16,
    25: 16,
    26: 17,
    27: 17,
    28: 18,
    29: 18,
    30: 19,
}


def estimator_player(draw):
    card = np.zeros(len(draw), dtype=int)
    for tile in draw:
        ideal_position = closest_positions[tile]
        empty_positions = np.where(card == 0)[0]
        distances = [abs(pos - ideal_position) for pos in empty_positions]
        card[empty_positions[np.argmin(distances)]] = tile
    return card


def estimator_v2_player(draw):
    #  if two positions are equally close, chose based on sign of tile - card[ideal_position]
    card = np.zeros(len(draw), dtype=int)
    for tile in draw:
        ideal_position = closest_positions[tile]
        empty_positions = np.where(card == 0)[0]
        best_position = np.array([abs(pos - ideal_position) for pos in empty_positions])
        min_idx = np.where(best_position == best_position.min())[0]
        if len(min_idx) == 1:
            use = min_idx[0]
        else:  # length == 2
            if card[ideal_position] < tile:
                use = min_idx.max()
            else:
                use = min_idx.min()
        card[empty_positions[use]] = tile
    return card


"""
# better?
class RandomPlayer(object):
    def __init__(self, ntiles=20):
        self.state = np.zeros(ntiles, dtype=int)
    def play(self, tile):
        available = np.where(self.state == 0)[0]
        idx = np.random.choice(available)
        self.state[idx] = tile
    def score(self):
        return game.score_board(self.state)
"""
