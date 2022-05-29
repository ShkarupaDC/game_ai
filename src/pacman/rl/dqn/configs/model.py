from dataclasses import dataclass

from .dqn import DQNConfig


@dataclass(eq=False)
class ModelConfig:
    dqn: DQNConfig
    memory: int
    lr: float
    batch_size: int
    gamma: float
    update_step: int
    model_path: str
    train_start: int
    print_every: int = 1
    device: str = "cuda"
