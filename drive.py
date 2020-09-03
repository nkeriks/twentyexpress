from absl import flags, logging, app
import numpy as np

import game
import players


FLAGS = flags.FLAGS

flags.DEFINE_string("player", "random", "random / sequential / estimator")
flags.DEFINE_integer("trials", 1000, "number of trials")


def main(argv):
    player_class = players.player_factory(FLAGS.player)
    if player_class is None:
        raise ValueError("No player named %s", FLAGS.player)

    res = np.zeros(FLAGS.trials, dtype=int)
    top_score = 0
    for n in range(FLAGS.trials):
        draw = game.draw()
        player = player_class()
        for tile in draw:
            player.play(tile)
        score = player.score()
        if score > top_score:
            top_score = score
            logging.info("game number = %s", n)
            logging.info("New max score of %s", score)
            logging.info("draw = %s", draw)
            logging.info("play = %s", player.state)
        res[n] = score

    logging.info("Did %s trials with player %s", FLAGS.trials, FLAGS.player)
    logging.info(
        "mean, median, min, max = %.2f, %.2f, %s, %s",
        res.mean(),
        np.median(res),
        res.min(),
        res.max(),
    )


if __name__ == "__main__":
    app.run(main)
