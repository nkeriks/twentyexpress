import game
import numpy as np
from absl import logging


def player_factory(player_name):
    if player_name == "random":
        return RandomPlayer
    elif player_name == "estimator":
        return EstimatorPlayer
    elif player_name == "estimator_v2":
        return EstimatorPlayerV2
    elif player_name == "estimator_v3":
        return EstimatorPlayerV3
    elif player_name == "estimator_v4":
        return EstimatorPlayerV4


class Player(object):
    # base class for players
    def __init__(self, num_positions=game.NUM_POSITIONS):
        self._available_code = 0
        self.state = np.zeros(num_positions, dtype=int)
        self.state[:] = self._available_code
        self.tiles_played = {x: 0 for x in game.VALUES}
        self.tiles_remaining = {x: (game.TILES == x).sum() for x in game.VALUES}

    def available_positions(self):
        return np.where(self.state == self._available_code)[0]

    def play(self, tile):
        raise NotImplementedError("players need to implement this")

    def place(self, tile, pos):
        self.state[pos] = tile
        self.tiles_played[tile] += 1
        self.tiles_remaining[tile] -= 1

    def score(self):
        return game.score_board(self.state)


class RandomPlayer(Player):
    # play randomly!
    def play(self, tile):
        logging.debug("pos = %s", self.available_positions())
        pos = np.random.choice(self.available_positions())
        self.place(tile, pos)


class EstimatorPlayer(Player):
    # list of positions from the kids
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

    def play(self, tile):
        ideal_position = self.closest_positions[tile]
        empty_positions = self.available_positions()
        distances = [abs(pos - ideal_position) for pos in empty_positions]
        self.place(tile, empty_positions[np.argmin(distances)])


class EstimatorPlayerV2(EstimatorPlayer):
    # deal with ties better
    def play(self, tile):
        ideal_position = self.closest_positions[tile]
        empty_positions = self.available_positions()
        best_position = np.array([abs(pos - ideal_position) for pos in empty_positions])
        min_idx = np.where(best_position == best_position.min())[0]
        if len(min_idx) == 1:
            use = min_idx[0]
        else:  # length == 2
            if self.state[ideal_position] < tile:
                use = min_idx.max()
            else:
                use = min_idx.min()
        self.place(tile, empty_positions[use])


empirical_positions = None


def generate_empirical_positions(trials=10000, do_round=True):
    counts = np.zeros(len(game.VALUES), dtype=int)
    sums = np.zeros(len(game.VALUES), dtype=int)

    for trial in range(10000):
        optimal = np.sort(game.draw())
        for position, tile in enumerate(optimal):
            counts[tile - 1] += 1
            sums[tile - 1] += position

    if do_round:
        ans = dict((t + 1, round(pos)) for (t, pos) in enumerate(sums / counts))
    else:
        ans = dict((t + 1, pos) for (t, pos) in enumerate(sums / counts))
    logging.info("generated closest positions as %s", ans)
    return ans


class EstimatorPlayerV3(EstimatorPlayerV2):
    # use an empirical list of closest_positions, rounded to ints
    def __init__(self):
        global empirical_positions
        if empirical_positions is None:
            empirical_positions = generate_empirical_positions(do_round=True)
        self.closest_positions = empirical_positions
        super().__init__()


class EstimatorPlayerV4(EstimatorPlayer):
    # use an empirical list of closest_positions, not rounded
    # due to lack of rounding, has to fall back to Estimator V1 decisions
    def __init__(self):
        global empirical_positions
        if empirical_positions is None:
            empirical_positions = generate_empirical_positions(do_round=False)
        self.closest_positions = empirical_positions
        super().__init__()
