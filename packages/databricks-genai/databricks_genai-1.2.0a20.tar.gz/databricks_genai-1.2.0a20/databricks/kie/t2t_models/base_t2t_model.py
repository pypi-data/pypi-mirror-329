"""Base class interface for T2T models."""

from abc import ABC, abstractmethod
from typing import Optional

from databricks.kie.t2t_schema import T2TSystemParams


class BaseT2TModel(ABC):
    """Abstract base class for text-to-text models."""

    @abstractmethod
    def __call__(self, model_input: str) -> str:
        """Generate prediction for the given input.
        
        Args:
            model_input: Input text to generate prediction for

        Returns:
            Generated prediction text
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_from_system_param(system_param: T2TSystemParams, **kwargs) -> Optional['BaseT2TModel']:
        """Create a model instance from a system parameter.
        
        Args:
            system_param: System parameter containing instruction and example data

        Returns:
            Instantiated model
        """
        raise NotImplementedError
