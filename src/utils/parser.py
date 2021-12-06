from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Pacman Game")

    parser.add_argument(
        "--layout", type=str, help="path to file with the map layout"
    )
    parser.add_argument(
        "--width", type=int, default=32, help="width of the maze"
    )
    parser.add_argument(
        "--height", type=int, default=32, help="height of the maze"
    )
    parser.add_argument(
        "--num-food",
        type=int,
        default=10,
        help="number of food sources in the maze",
    )
    parser.add_argument(
        "--num-ghosts",
        type=int,
        default=1,
        help="number of ghosts in the maze",
    )
    parser.add_argument(
        "--log-path",
        type=str,
        default="logs/log.csv",
        help="path to file to write logs in",
    )
    parser.add_argument(
        "--max-num-ghosts",
        type=int,
        help="the maximum number of ghosts to use",
        default=2,
    )
    parser.add_argument(
        "--zoom",
        type=float,
        help="zoom the size of the graphics window",
        default=1.0,
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="fixes the random seed to always play the same game",
    )
    parser.add_argument(
        "--frame-time",
        type=float,
        help="time to delay between frames; 0 means keyboard",
        default=0.1,
    )
    parser.add_argument(
        "--num-games",
        type=int,
        help="number of consecutive games to play ",
        default=1,
    )
    return parser
