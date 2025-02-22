from pathlib import Path
from typing import Any, Callable, Iterator, List, Union, TypeVar, overload
from dyncfg import ConfigValue

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec



class ConfigValueList:
    """
    A wrapper for a list of ConfigValue objects that supports method chaining.
    This stub provides type hints for intellisense and static analysis.
    """

    values: List[ConfigValue]

    def __init__(self, values: List[ConfigValue]) -> None: ...

    def __iter__(self) -> Iterator[ConfigValue]: ...

    @overload
    def __getitem__(self, index: int) -> ConfigValue: ...

    @overload
    def __getitem__(self, index: slice) -> "ConfigValueList": ...

    def __repr__(self) -> str: ...

    def __getattr__(self, name: str) -> Callable[..., Union["ConfigValueList", List[Any]]]: ...

    def as_int(self, default: int=0) -> List[int]: ...

    def as_float(self, default: float=0.0) -> List[float]: ...

    def as_bool(self, default: bool=False) -> List[bool]: ...

    def as_path(self) -> List[Path]: ...

    R = TypeVar('R')

    def apply(self, function: Callable[..., R], *args, **kwargs) -> List[Union[ConfigValue, R]]: ...