from dataclasses import dataclass


@dataclass(eq=False)
class LinearParams:
    in_features: int
    out_features: int
