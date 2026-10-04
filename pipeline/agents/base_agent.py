from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Base class for repository agents."""

    name: str = "base-agent"
    description: str = "Generic agent placeholder"

    @abstractmethod
    def run(self, payload: Any) -> Any:
        raise NotImplementedError
