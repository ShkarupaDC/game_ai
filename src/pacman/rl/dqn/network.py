import torch
import torch.nn as nn
from torchsummary import summary
from dataclasses import asdict
from typing import Optional

from .configs.dqn import DQNConfig
from .utils.layer_params import LinearParams, ConvParams


def conv(params: ConvParams, pool: bool = True) -> nn.Module:
    layers = [
        nn.Conv2d(**asdict(params)),
        nn.ReLU(inplace=True),
        nn.BatchNorm2d(params.out_channels),
    ]
    if pool is True:
        layers.append(nn.MaxPool2d(2, 2))
    return nn.Sequential(*layers)


def linear(params: LinearParams, dropout: Optional[float] = None) -> nn.Module:
    layers = [nn.Linear(**asdict(params))]
    if dropout is not None:
        layers.append(nn.Dropout(dropout))
    layers.append(nn.ReLU(inplace=True))
    return nn.Sequential(*layers)


class DQN(nn.Module):
    def __init__(self, config: DQNConfig) -> None:
        super().__init__()
        num_features = self.__get_num_features(config.width, config.height)
        self.network = nn.Sequential(
            conv(ConvParams(config.in_channels, 8)),
            conv(ConvParams(8, 16)),
            conv(ConvParams(16, 32)),
            nn.Flatten(),
            linear(LinearParams(num_features, 64), dropout=0.5),
            linear(LinearParams(64, config.out_features)),
        )
        self.config = config

    def __get_num_features(self, width: int, height: int) -> int:
        num_channles, reduce_by = 32, 8
        width = width // reduce_by
        height = height // reduce_by
        return int(width * height * num_channles)

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        return self.network(state)


if __name__ == "__main__":
    shape = in_channels, width, height = 4, 24, 32
    model = DQN(width, height, in_channels)
    summary(model, shape, device="cpu")
