import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from pathlib import Path
from dataclasses import asdict

from .network import DQN
from .configs.model import ModelConfig
from .utils.experience import Experience
from .utils.replay_memory import ReplayMemory
from ....utils.general import to_numpy


class Model:
    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        self.memory = ReplayMemory(config.memory)

        self.policy_net = DQN(config.dqn).to(config.device)
        self.target_net = DQN(config.dqn).to(config.device)

        self.criterion = nn.SmoothL1Loss()
        self.optimizer = Adam(self.policy_net.parameters(), lr=config.lr)

        self.step: int = 0
        self.history: list[float] = []

        self.load_checkpoint(update_target_net=True)
        self.target_net.eval()

    def evaluate(self, state: np.ndarray) -> np.ndarray:
        state = torch.tensor(state[np.newaxis, :], device=self.config.device)
        with torch.no_grad():
            values = self.policy_net(state)[0]
        return to_numpy(values)

    def __get_train_batch(self) -> dict[str, torch.Tensor]:
        samples = self.memory.sample(self.config.batch_size)
        batch = {
            key: torch.tensor(
                np.array(
                    [getattr(sample, key) for sample in samples],
                ),
                device=self.config.device,
            )
            for key in asdict(samples[0])
        }
        return batch

    def train(self, experience: Experience) -> None:
        self.memory.push(experience)
        config = self.config

        if len(self.memory) >= config.train_start:
            batch = self.__get_train_batch()
            self.step += 1
            self.optimizer.zero_grad()

            action_idxs = batch["action"].view(-1, 1)
            values = self.policy_net(batch["state"]).gather(1, action_idxs)
            next_values = torch.zeros(config.batch_size, device=config.device)
            terminal = batch["terminal"]

            non_terminal = batch["next_state"][~terminal]
            next_values[~terminal] = (
                self.target_net(non_terminal).max(dim=1)[0].detach()
            )
            expected_values = next_values * config.gamma + batch["reward"]
            loss = self.criterion(values, expected_values.unsqueeze(1))

            loss.backward()
            self.optimizer.step()
            self.history.append(loss.item())

            if self.step % config.update_step == 0:
                self.__update_target_net()

            if self.step % config.print_every == 0:
                print("Step:", self.step, "Loss:", loss.item())

    def __update_target_net(self) -> None:
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save_checkpoint(self) -> None:
        state_dict = {
            name: getattr(self, name).state_dict()
            for name in ["policy_net", "target_net", "optimizer"]
        }
        state_dict["step"] = self.step
        torch.save(state_dict, self.config.model_path)

    def load_checkpoint(self, update_target_net: bool = False) -> None:
        config = self.config
        if Path(config.model_path).exists():
            checkpoint = torch.load(
                config.model_path, map_location=config.device
            )
            for name in ["policy_net", "target_net", "optimizer"]:
                getattr(self, name).load_state_dict(checkpoint[name])
            self.step = checkpoint["step"]
        else:
            if update_target_net:
                self.__update_target_net()
