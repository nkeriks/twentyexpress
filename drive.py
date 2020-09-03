from absl import flags, logging, app
import numpy as np

import game
import players


FLAGS = flags.FLAGS

flags.DEFINE_string("player", "random", "random / sequential / estimator")
flags.DEFINE_integer("trials", 1000, "number of trials")


def main(argv):

    if FLAGS.player == "random":
        player = players.random_player
    elif FLAGS.player == "sequential":
        player = players.sequential_player
    elif FLAGS.player == "estimator":
        player = players.estimator_player
    elif FLAGS.player == "estimator_v2":
        player = players.estimator_v2_player

    res = np.zeros(FLAGS.trials, dtype=int)
    top_score = 0
    for n in range(FLAGS.trials):
        draw = game.draw()
        play = player(draw)
        score = game.score_board(play)
        if score > top_score:
            top_score = score
            logging.info("game number = %s", n)
            logging.info("New max score of %s, board = %s", score, play)
            logging.info("draw = %s", draw)
            logging.info("play = %s", play)
        res[n] = score

    logging.info("Did %s trials with player %s", FLAGS.trials, FLAGS.player)
    logging.info("mean, min, max = %s, %s, %s", res.mean(), res.min(), res.max())


if __name__ == "__main__":
    app.run(main)
