"""Registry for T2T models."""

import inspect
from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional, Union

import catalogue

from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_schema import T2TSystemParams


@dataclass
class T2TModelConfig:
    """Model config for model in T2T model registry."""
    name: str
    is_default: bool
    model: BaseT2TModel


class DefaultModelConfig(NamedTuple):
    """Configuration for the default T2T model."""
    name: str
    factory: Callable[[T2TSystemParams], BaseT2TModel]


class T2TModelRegistry(catalogue.Registry):
    """A thin wrapper around catalogue.Registry to add T2T models."""

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.default_model: Optional[DefaultModelConfig] = None

    def __call__(self, name: str, is_default: bool = False) -> BaseT2TModel:
        """Register a model to the registry."""
        if is_default and self.default_model:
            raise ValueError("Only one default model can be registered")

        def _wrapper(cls):
            self.register(name, to_register=cls, is_default=is_default)
            return cls

        return _wrapper

    def register(self,
                 name: str,
                 *,
                 to_register: Union[Callable[[T2TSystemParams], BaseT2TModel], BaseT2TModel],
                 is_default: bool = False):
        """Register a model to the registry."""
        if is_default and self.default_model:
            raise ValueError("Only one default model can be registered")

        if isinstance(to_register, type):
            # if register is a class, then it must implement BaseT2TModel
            if not issubclass(to_register, BaseT2TModel):
                raise ValueError("If registering a class, it must implement BaseT2TModel")

            func = to_register.create_from_system_param
        else:
            func = to_register

        # Inspect function signature
        sig = inspect.signature(func)
        params = sig.parameters
        # Get non-bounded arguments (exclude self/cls)
        non_bounded_args = [
            p for p in params.values() if p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD, p.KEYWORD_ONLY)
        ]
        if len(non_bounded_args) != 1:
            raise ValueError(f"Function {func.__name__} must have exactly 1 non-bounded argument")
        # Check argument type annotation
        arg = non_bounded_args[0]
        if arg.annotation != T2TSystemParams:
            raise ValueError("Argument of registered function must be 1 argument of type T2TSystemParams")

        if is_default:
            self.default_model = DefaultModelConfig(name=name, factory=func)

        return super().register(name, func=func)


model_registry = T2TModelRegistry("t2t_model_registry")
