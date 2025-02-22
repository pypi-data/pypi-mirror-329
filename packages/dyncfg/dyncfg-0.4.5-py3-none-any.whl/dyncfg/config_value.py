import functools
import logging
from pathlib import Path
from typing import Callable, Union, TypeVar

from dyncfg.config_value_list import ConfigValueList

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

logger = logging.getLogger(__name__)


class ConfigValue(str):
    """A subclass of str that provides additional methods for type conversion and default handling.

    Attributes:
        parent (DynamicConfig): The parent configuration instance.
        section (str): The section name in the configuration.
        key (str): The key name in the section.
    """

    def __new__(cls, value: str, parent=None, section: str = None, key: str = None) -> "ConfigValue":
        obj = super(ConfigValue, cls).__new__(cls, value)
        obj.parent = parent
        obj.section = section
        obj.key = key

        obj._wrapped_cache = {}
        return obj

        return obj

    def _with_context(self, value: str) -> "ConfigValue":
        """
        Helper method to create a new ConfigValue with the same context.
        """
        return ConfigValue(value, self.parent, self.section, self.key)

    def __getattribute__(self, name):
        """
        Intercept attribute access to dynamically wrap any string method that returns a string
        with the same context. This version caches the wrapped methods to optimise performance.
        """
        # Bypass wrapping for special dunder attributes for safety and performance.
        if name.startswith("__") and name.endswith("__"):
            return super().__getattribute__(name)

        # Retrieve the cache of wrapped methods.
        _wrapped_cache = super().__getattribute__("_wrapped_cache")
        if name in _wrapped_cache:
            return _wrapped_cache[name]

        attr = super().__getattribute__(name)
        # Check if the attribute is callable and exists on the base str type.
        if callable(attr) and hasattr(str, name):
            @functools.wraps(attr)
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if isinstance(result, str):
                    return self._with_context(result)
                return result

            # Cache the wrapped method for future accesses.
            _wrapped_cache[name] = wrapper
            return wrapper

        return attr



    def or_default(self, default_value, update: bool = True) -> "ConfigValue":
        """Return the value if non-empty; otherwise, return and optionally update with default_value."""
        if self:
            return self  # Return current non-empty value.

        if update and self.parent and self.section and self.key:
            with self.parent._lock:
                self.parent.config.set(self.section, self.key, str(default_value))
                if self.parent.auto_write:
                    self.parent._write_config()
        return ConfigValue(str(default_value), self.parent, self.section, self.key)

    def log(self) -> "ConfigValue":
        """Log the configuration value."""
        logger.info(f"[{self.section}] {self.key} = {self}")
        return self

    def as_int(self, default: int = 0) -> int:
        """Convert the value to an integer, or return a default value if conversion fails."""
        try:
            return int(self)
        except ValueError:
            logger.error(f"Error converting '{self}' to an integer")
            return default

    def as_float(self, default: float = 0.0) -> float:
        """Convert the value to a float, or return a default value if conversion fails."""
        try:
            return float(self)
        except ValueError:
            logger.error(f"Error converting '{self}' to a float")
            return default

    def as_bool(self, default: bool = False) -> bool:
        """Convert the value to a boolean, or return a default value if conversion fails."""
        val = self.lower()
        if val in ("true", "yes", "1"):
            return True
        elif val in ("false", "no", "0"):
            return False
        logger.error(f"Error converting '{self}' to a boolean")
        return default

    def as_path(self) -> Path:
        """Convert the value to a path"""
        val = Path(self)

        return val

    def as_list(self, separator: str = ",") -> "ConfigValueList":
        """
        Convert the string value into a ConfigValueList by splitting on the given separator.

        Args:
            separator (str): The delimiter to use for splitting the string. Defaults to a comma.

        Returns:
            ConfigValueList: A list-like wrapper of ConfigValue objects.
        """

        values = [
            ConfigValue(item.strip(), self.parent, self.section, self.key)
            for item in self.split(separator)
        ]
        return ConfigValueList(values)

    R = TypeVar('R')

    def apply(self, function: Callable[..., R], *args, **kwargs) -> Union["ConfigValue", R]:
        """
        Call a function using this ConfigValue as the first argument.

        If the function returns a string, it is wrapped in a new ConfigValue with the same context.

        Args:
            function (Callable[..., R]):
                A function that takes this ConfigValue (or its string form) as its first parameter.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            Union[ConfigValue, R]: A ConfigValue if the result is a string; otherwise, the raw result.
        """
        result = function(self, *args, **kwargs)
        if isinstance(result, str):
            return self._with_context(result)
        return result