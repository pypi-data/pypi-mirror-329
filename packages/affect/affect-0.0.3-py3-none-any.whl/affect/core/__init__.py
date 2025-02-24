"""Core module for affect."""

from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict

from affect.typings import F, S


class _ResultBase(BaseModel, ABC):
    """Base class for results."""

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def is_ok(self) -> bool:
        """Check if the result is ok."""


class Success(_ResultBase, Generic[S]):
    """A successful result."""

    value: S

    def is_ok(self) -> Literal[True]:
        """Check if the success is ok."""
        return True


class Failure(_ResultBase, Generic[F]):
    """A failed result."""

    value: F

    def is_ok(self) -> Literal[False]:
        """Check if the failure is ok."""
        return False


Result: TypeAlias = Success[S] | Failure[F]
