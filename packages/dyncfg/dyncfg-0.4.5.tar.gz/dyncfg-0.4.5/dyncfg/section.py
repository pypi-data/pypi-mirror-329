from dyncfg.config_value import ConfigValue
import logging

logger = logging.getLogger(__name__)

class Section:
    """A class representing a section within the configuration file."""

    def __init__(self, parent, name: str):
        self.parent = parent
        self.name = name

    def __getattr__(self, key: str) -> ConfigValue:
        """Retrieve a configuration value. If the key does not exist, create it with an empty value."""
        with self.parent._lock:
            if self.parent.config.has_option(self.name, key):
                value = self.parent.config.get(self.name, key)
            else:
                logger.debug(f"Key '{key}' not found in section '{self.name}'. Creating it with an empty value.")
                self.parent.config.set(self.name, key, "")
                if self.parent.auto_write:
                    self.parent._write_config()
                value = ""
            return ConfigValue(value, self.parent, self.name, key)

    def __setattr__(self, key: str, value: str):
        if key in ("parent", "name"):
            super().__setattr__(key, value)
        else:
            with self.parent._lock:
                if not self.parent.config.has_section(self.name):
                    self.parent.ensure_section(self.name)
                self.parent.config.set(self.name, key, value)
                if self.parent.auto_write:
                    self.parent._write_config()

    def __getitem__(self, key: str) -> ConfigValue:
        """Allow dictionary-style access for keys."""
        return self.__getattr__(key)

    def __setitem__(self, key: str, value: str):
        """Allow dictionary-style setting of keys."""
        self.__setattr__(key, value)

    def remove(self, key: str):
        """Remove a key from this section."""
        with self.parent._lock:
            if self.parent.config.has_option(self.name, key):
                self.parent.config.remove_option(self.name, key)
                if self.parent.auto_write:
                    self.parent._write_config()

    def keys(self):
        """Return a list of all keys in this section."""
        with self.parent._lock:
            if self.parent.config.has_section(self.name):
                return list(self.parent.config.options(self.name))
            return []
