from typing import Any, Callable, List, Union, TypeVar, Generic, Iterator

T = TypeVar('T')


class ConfigValueList(Generic[T]):
    """A wrapper for a list of items (typically ConfigValue objects) that supports method chaining."""

    def __init__(self, values: List[T]) -> None:
        self.values = list(values)

    def __iter__(self) -> Iterator[T]:
        return iter(self.values)

    def __getitem__(self, index: Union[int, slice]) -> Union["ConfigValue", "ConfigValueList"]:

        result = self.values[index]
        if isinstance(index, slice):
            return ConfigValueList(result)
        return result

    def __repr__(self) -> str:
        return f"ConfigValueList({self.values!r})"

    def __getattr__(self, name: str) -> Callable[..., Union["ConfigValueList[T]", List[Any]]]:
        """
        Dynamically delegate attribute access to each element in the list.

        If the delegated call returns a ConfigValue for every element,
        wrap the results in a new ConfigValueList (to allow method chaining);
        otherwise, return a list of results.
        """
        from dyncfg import ConfigValue  # Assuming ConfigValue is defined in dyncfg

        def method(*args: Any, **kwargs: Any) -> Union["ConfigValueList[T]", List[Any]]:
            results = [getattr(value, name)(*args, **kwargs) for value in self.values]
            if all(isinstance(result, ConfigValue) for result in results):
                return ConfigValueList(results)
            else:
                return results

        return method
