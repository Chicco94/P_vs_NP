from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseSolver(ABC):
    """Abstract interface for TSP algorithm prototypes."""

    def __init__(self, instance: Iterable[Any]):
        self.instance = list(instance)

    @abstractmethod
    def solve(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    def metrics(self) -> dict[str, Any]:
        raise NotImplementedError
