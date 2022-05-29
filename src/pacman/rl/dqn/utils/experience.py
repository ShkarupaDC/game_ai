import numpy as np
from dataclasses import dataclass


@dataclass(eq=False)
class Experience:
    state: np.ndarray
    action: int
    next_state: np.ndarray
    reward: float
    terminal: bool
