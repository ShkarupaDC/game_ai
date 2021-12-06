import random
from pathlib import Path
from typing import Any

from src.pacman.keyboard_agents import KeyboardAgent
from src.pacman.multiagent.agents import MinimaxAgent, ExpectimaxAgent
from src.pacman.search.agents import FourPointAgent, AllFoodAgent
from src.pacman.rl import (
    DQNAgent,
    DQNAgentConfig,
    ModelConfig,
    DQNConfig,
    EpsParams,
)
from src.pacman.ghost_agents import GreedyGhost, RandomGhost
from src.pacman.rules import GameRules
from src.graphics import display
from src.utils.layout import Layout
from src.utils.parser import get_parser
from src.consts.types import Params


def parse_args() -> tuple[Params, Params]:
    parser = get_parser()
    options = parser.parse_args()

    layout_keys = ["width", "height", "num_food", "num_ghosts", "layout"]
    layout_params = {key: getattr(options, key) for key in layout_keys}

    args = {"num_games": options.num_games}
    # ExpectimaxAgent() MinimaxAgent(), KeyboardAgent(), FourPointAgent(), AllFoodAgent()
    agent_config = DQNAgentConfig(
        model=ModelConfig(
            dqn=DQNConfig(
                width=layout_params["width"],
                height=layout_params["height"],
                in_channels=4,
                out_features=4,
            ),
            memory=10000,
            lr=2e-4,
            batch_size=64,
            gamma=0.999,
            update_step=200,
            device="cpu",
            train_start=2000,
            model_path="src/pacman/rl/dqn/trained/checkpoint.tar.pth",
        ),
        eps_params=EpsParams(start=0.9, end=0.05, step=10000),
        train=True,
    )
    args["pacman_agent"] = DQNAgent(agent_config)
    args["ghost_agents"] = [
        GreedyGhost(idx + 1) for idx in range(options.max_num_ghosts)
    ]
    args["display"] = display.PacmanGraphics(
        zoom=options.zoom, frame_time=options.frame_time
    )
    if options.seed is not None:
        random.seed(options.seed)
    args["log_path"] = Path(options.log_path)
    return args, layout_params


def generate_layout(params: dict[str, Any]) -> Layout:
    layout = (
        Layout.generate(
            height=params["height"],
            width=params["width"],
            num_food=params["num_food"],
            num_ghosts=params["num_ghosts"],
        )
        if params["layout"] is None
        else Layout.from_text(params["layout"].layout)
    )
    if layout is None:
        raise Exception("Invalid layout parameters")
    return layout


if __name__ == "__main__":
    args, layout_params = parse_args()
    rules = GameRules()

    num_games = args.pop("num_games")
    for idx in range(num_games):
        args["layout"] = generate_layout(layout_params)
        game = rules.new_game(**args)
        game.run()
