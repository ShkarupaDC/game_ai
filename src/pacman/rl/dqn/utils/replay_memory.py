import random
from collections import deque

from .experience import Experience


class ReplayMemory:
    def __init__(self, capacity: int) -> None:
        self.memory = deque(maxlen=capacity)

    def push(self, experience: Experience) -> None:
        self.memory.append(experience)

    def sample(self, batch_size: int) -> list[Experience]:
        return random.sample(self.memory, batch_size)

    def __len__(self) -> int:
        return len(self.memory)
