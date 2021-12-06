from dataclasses import dataclass, field


@dataclass(eq=False)
class ConvParams:
    in_channels: int
    out_channels: int
    kernel_size: int = 3
    stride: int = 1
    padding: int = field(init=False)

    def __post_init__(self) -> None:
        self.padding = (self.kernel_size - 1) // 2
