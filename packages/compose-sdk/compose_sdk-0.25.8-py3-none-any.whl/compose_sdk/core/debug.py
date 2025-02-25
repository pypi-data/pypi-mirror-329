from contextlib import contextmanager, asynccontextmanager
import datetime
import time
from typing import Callable, Generator, AsyncGenerator


class Debug:
    @staticmethod
    def log(type: str, message: str) -> None:
        print(
            f"{type} event | {message} | {datetime.datetime.now().isoformat(timespec='milliseconds')}"
        )

    @staticmethod
    @contextmanager
    def measure_duration(
        message: Callable[[float], str]
    ) -> Generator[None, None, None]:
        start = time.perf_counter()

        try:
            yield
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            message(elapsed)

    @staticmethod
    @asynccontextmanager
    async def async_measure_duration(
        message: Callable[[float], str]
    ) -> AsyncGenerator[None, None]:
        start = time.perf_counter()

        try:
            yield
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            message(elapsed)
