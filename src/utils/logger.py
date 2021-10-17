import csv
from pathlib import Path
from dataclasses import dataclass

from .general import sort_dict
from ..consts.types import GameResult


@dataclass(eq=False)
class Logger:
    log_path: Path
    delimiter: str = ","
    mode: str = "a"

    def __post_init__(self) -> None:
        self.header = not self.log_path.exists()

    def log_result(self, result: GameResult) -> None:
        result = sort_dict(result)
        with open(self.log_path, mode=self.mode) as log_file:
            writer = csv.DictWriter(
                log_file, fieldnames=result.keys(), delimiter=self.delimiter
            )
            if self.header:
                writer.writeheader()
            writer.writerow(result)
