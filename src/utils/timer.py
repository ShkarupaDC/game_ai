import time
from functools import wraps
from typing import Any, Callable


class Timer:
    def __init__(self) -> None:
        self.reset()

    @property
    def elapsed(self) -> float:
        return self._elapsed

    def start(self) -> None:
        self._start = time.perf_counter()

    def stop(self) -> None:
        self._elapsed = time.perf_counter() - self._start

    def reset(self) -> None:
        self._start = 0
        self._elapsed = 0


def time_it(stdout: bool = False) -> Callable:
    def timer(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            result = function(*args, **kwargs)
            end = time.perf_counter()
            if stdout is True:
                print(f"Time ({function.__name__}):", end - start)
            return result

        return wrapper

    return timer
