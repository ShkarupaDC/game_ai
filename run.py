import argparse
import random
from pathlib import Path

from src.utils.layout import Layout
from src.pacman.keyboard_agents import KeyboardAgent
from src.pacman.multiagent.agents import MinimaxAgent, ExpectimaxAgent
from src.pacman.search.agents import FourPointAgent, AllFoodAgent
from src.pacman.ghost_agents import GreedyGhost, RandomGhost
from src.pacman.rules import GameRules
from src.graphics import display


def parse_args():
    parser = argparse.ArgumentParser(description="Pacman Game")

    parser.add_argument(
        "-l",
        "--layout",
        help="path to file with the map layout",
    )
    parser.add_argument(
        "--log-path",
        type=str,
        default="logs/log.csv",
        help="path to file to write logs in",
    )
    parser.add_argument(
        "-g",
        "--num-ghosts",
        type=int,
        help="the maximum number of ghosts to use",
        default=2,
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        help="zoom the size of the graphics window",
        default=1.0,
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="fixes the random seed to always play the same game",
    )
    parser.add_argument(
        "--frame-time",
        type=float,
        help="time to delay between frames; <0 means keyboard",
        default=0.1,
    )
    options = parser.parse_args()

    layout = (
        Layout.from_text(options.layout)
        if options.layout is not None
        else Layout.generate(height=32, width=32, num_food=10, num_ghosts=1)
    )
    if layout is None:
        raise Exception(f"The layout {options.layout} cannot be found")
    args = {"layout": layout}

    # MinimaxAgent(), KeyboardAgent(), FourPointAgent(), AllFoodAgent()
    args["pacman_agent"] = ExpectimaxAgent()
    args["ghost_agents"] = [
        GreedyGhost(idx + 1) for idx in range(options.num_ghosts)
    ]
    args["display"] = display.PacmanGraphics(
        zoom=options.zoom, frame_time=options.frame_time
    )
    if options.seed is not None:
        random.seed(options.seed)
    args["log_path"] = Path(options.log_path)
    return args


if __name__ == "__main__":
    args = parse_args()
    rules = GameRules()
    game = rules.new_game(**args)
    game.run()
