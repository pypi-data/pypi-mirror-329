import configparser
import os
import threading
import logging
from pathlib import Path
from typing import Union

from dyncfg.section import Section

logger = logging.getLogger(__name__)

class DynamicConfig:
    """A class to manage dynamic configuration settings using an INI file."""

    def __init__(self, filename: Union[str | Path], default_section: str = "Default", auto_write: bool = True):
        self.filename = Path(filename).resolve(strict=False)
        self.default_section = default_section
        self.auto_write = auto_write  # Determines if changes are written immediately.
        self.config = configparser.ConfigParser()
        self._lock = threading.RLock()  # Use RLock for nested locking.
        self._read_config()

    def _read_config(self):
        with self._lock:
            try:
                if os.path.exists(self.filename):
                    self.config.read(self.filename, encoding="utf-8")
                else:
                    # Create an empty file if it does not exist.
                    with open(self.filename, "w", encoding="utf-8") as f:
                        pass
            except Exception as e:
                logger.error(f"Error reading config file '{self.filename}': {e}")

    def _write_config(self):
        with self._lock:
            try:
                with open(self.filename, "w", encoding="utf-8") as configfile:
                    self.config.write(configfile)
            except Exception as e:
                logger.error(f"Error writing config file '{self.filename}': {e}")

    def reload(self):
        """Reload the configuration from the file."""
        self._read_config()

    def ensure_section(self, section: str):
        with self._lock:
            if not self.config.has_section(section):
                self.config.add_section(section)
                if self.auto_write:
                    self._write_config()

    def remove_key(self, section: str, key: str):
        """Remove a key from a given section."""
        with self._lock:
            if self.config.has_section(section) and self.config.has_option(section, key):
                self.config.remove_option(section, key)
                if self.auto_write:
                    self._write_config()

    def remove_section(self, section: str):
        """Remove an entire section."""
        with self._lock:
            if self.config.has_section(section):
                self.config.remove_section(section)
                if self.auto_write:
                    self._write_config()

    def update_section(self, section: str, data: dict):
        """Batch update keys in a section from a dictionary.

        Args:
            section (str): The section to update.
            data (dict): A dictionary of key-value pairs to update.
        """
        with self._lock:
            self.ensure_section(section)
            for key, value in data.items():
                self.config.set(section, key, str(value))
            if self.auto_write:
                self._write_config()

    def get_section(self, section: str) -> Section:
        """Return a Section object for the given section name."""
        with self._lock:
            self.ensure_section(section)
            return Section(self, section)

    def __getitem__(self, section: str) -> Section:
        """Allow dictionary-style access for sections."""
        return self.get_section(section)

    def __getattr__(self, name: str):
        """Enable dynamic access for keys in the default section.

        Note: This is only called if the attribute is not found normally.
        """
        return self.get_section(self.default_section).__getattr__(name)

    def __setattr__(self, name: str, value):
        """Enable dynamic setting of keys in the default section,
        except for internal attributes.
        """
        if name in ("filename", "default_section", "config", "_lock", "auto_write"):
            super().__setattr__(name, value)
        else:
            self.get_section(self.default_section).__setattr__(name, value)

    def save(self):
        """Save all pending changes to the configuration file.

        This method is useful when auto_write is disabled (i.e., auto_write=False).
        Call this method to manually write all configuration changes to disk.
        """
        with self._lock:
            self._write_config()
