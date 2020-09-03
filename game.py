import numpy as np

NUM_POSITIONS = 20
SCORES = {
    1: 0,
    2: 1,
    3: 3,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
    8: 15,
    9: 20,
    10: 25,
    11: 30,
    12: 35,
    13: 40,
    14: 50,
    15: 60,
    16: 70,
    17: 85,
    18: 100,
    19: 150,
    20: 300,
}

score_array = np.array([SCORES.get(i, 0) for i in range(21)])

VALUES = np.arange(1, 31)
STAR = -1
TILES = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    11,
    12,
    12,
    13,
    13,
    14,
    14,
    15,
    15,
    16,
    16,
    17,
    17,
    18,
    18,
    19,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
]  # , STAR, ]


def fill_star(board):
    if STAR in board:
        idx = np.where(board == STAR)[0][0]
        ret = []
        for val in VALUES:
            tmp = board.copy()
            tmp[idx] = val
            ret.append(tmp)
        return ret
    else:
        return [board]


def score_star_board(board):
    logging.info("scoring %s", board)
    possible_boards = fill_star(board)
    scores = np.array([score_board(b) for b in possible_boards])
    logging.debug(zip(scores, possible_boards))
    return scores.max()


def score_board(x):
    breakpoints = np.where(x[:-1] > x[1:])[0]
    breakpoints = np.concatenate(([-1], breakpoints, [len(x) - 1]))
    lengths = breakpoints[1:] - breakpoints[:-1]
    return score_array[breakpoints[1:] - breakpoints[:-1]].sum()


def draw():
    return np.random.choice(TILES, size=NUM_POSITIONS, replace=False)
