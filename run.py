import argparse
import random

from src.utils.layout import Layout
from src.pacman.keyboard_agents import KeyboardAgent
from src.pacman.ghost_agents import RandomGhost
from src.pacman.rules import GameRules
from src.graphics import display
from src.graphics.ui import UI


def parse_args():
    parser = argparse.ArgumentParser(description="Pacman Game")

    parser.add_argument(
        "-l",
        "--layout",
        help="file from which to load the map layout",
        default="medium",
    )
    parser.add_argument(
        "-k",
        "--num-ghosts",
        type=int,
        help="The maximum number of ghosts to use",
        default=2,
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        help="Zoom the size of the graphics window",
        default=1.0,
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Fixes the random seed to always play the same game",
    )
    parser.add_argument(
        "--frame-time",
        type=float,
        help="Time to delay between frames; <0 means keyboard",
        default=0.1,
    )
    options = parser.parse_args()
    args = {}
    if options.seed is not None:
        random.seed(options.seed)

    args["layout"] = Layout.get_layout(options.layout)
    if args["layout"] == None:
        raise Exception(f"The layout {options.layout} cannot be found")

    args["ghost_agents"] = [
        RandomGhost(idx + 1) for idx in range(options.num_ghosts)
    ]
    args["pacman_agent"] = KeyboardAgent()

    args["display"] = display.PacmanGraphics(
        UI(), zoom=options.zoom, frame_time=options.frame_time
    )
    return args


if __name__ == "__main__":
    args = parse_args()
    rules = GameRules()
    game = rules.new_game(**args)
    game.run()
