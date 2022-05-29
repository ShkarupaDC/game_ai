from dataclasses import dataclass


@dataclass(eq=False)
class DQNConfig:
    width: int
    height: int
    in_channels: int
    out_features: int = 4
