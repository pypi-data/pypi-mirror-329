# DynCFG Documentation

`dyncfg` is a flexible system for managing configuration settings using INI files. It supports both dot notation and dictionary-style access, type conversion, batch updates, auto-reloading, and thread safety. At its core, it is a wrapper around configparser built for humans to reduce mental-load and boilerplate.

## TLDR

This package lets you use configuration files like this:

```Python
from dyncfg import DynamicConfig

config = DynamicConfig('my_config.ini')

# Setting values
config.section1.key1 = "value1"
config['section2']['key2'] = 123

# Getting values with type conversion and default values
name = config.user.name.or_default("guest")
port = config.network.port.as_int(8080)
debug_mode = config.debug.enabled.as_bool(False)

# logging a value as we load it
experimental_setting = config["debug"]["experiment"].or_default(False).log().as_bool()


# Removing keys and sections
config.section1.remove('key1')
config.remove_section('section2')
```


## Features

- **Dynamic Attribute Access:**  
  Retrieve and set configuration values using dot notation (e.g. `dc.setting = "test"`).

- **Dictionary-Style Access:**  
  Access sections and keys using indexing (e.g. `dc["section1"]["someKey"]`).

- **Type Conversion:**  
  Convert configuration values to integer, float, or boolean using methods like `as_int()`, `as_float()`, and `as_bool()`.

- **Default Values:**  
  Use the `or_default()` method to provide default values if a key is empty, with an optional flag to update the configuration.

- **Batch Updates:**  
  Update multiple keys in a section at once with a dictionary.

- **Auto-Reload:**  
  Reload the configuration file if it has been modified externally.

- **Removal Methods:**  
  Remove individual keys or entire sections from the configuration.

- **Thread Safety:**  
  Built-in locking ensures that reading and writing to the configuration file is thread-safe.

## Installation

You can install `dyncfg` using pip:

```bash
pip install dyncfg
```

## Usage

### Basic Usage

```python
from dyncfg import DynamicConfig

# Initialise the configuration with an INI file.
dc = DynamicConfig("config.ini")

# Set a value in the default section using dot notation.
dc.setting = "test"

# Retrieve a value from the default section.
print(dc.setting)  # Output: test

# Use a default value if a key is empty (without updating the configuration).
print(dc.setting2.or_default("defaultValue"))

# Use a default value and update the configuration if the key is empty.
print(dc.setting3.or_default("newDefault", update=True))
```

### Accessing Explicit Sections

```python
from dyncfg import DynamicConfig
dc = DynamicConfig("config.ini")
# Set a value in a specific section.
dc["section1"].someSetting = "setValue"

# Retrieve a value from that section using dictionary-style access.
print(dc["section1"]["someSetting"].or_default("defaultVal"))  # Output: setValue
```

### Type Conversion

```python
from dyncfg import DynamicConfig
dc = DynamicConfig("config.ini")
# Retrieve a configuration value as an integer.
dc.number = "42"
print(dc.number.as_int())  # Output: 42

# Retrieve a configuration value as a float.
dc.pi = "3.14"
print(dc.pi.as_float())  # Output: 3.14

# Retrieve a configuration value as a boolean.
dc.enabled = "true"
print(dc.enabled.as_bool())  # Output: True
```

### Batch Updates and Removal

```python
from dyncfg import DynamicConfig
dc = DynamicConfig("config.ini")
# Batch update a section with a dictionary.
dc.update_section("section2", {"key1": "value1", "key2": "42"})

# Remove a specific key from a section.
dc.remove_key("section2", "key1")

# Remove an entire section.
dc.remove_section("section2")
```

### Auto-Reload

```python
from dyncfg import DynamicConfig
dc = DynamicConfig("config.ini")
# Reload configuration from disk.
dc.reload()
```

## API Reference

### DynamicConfig

- **`__init__(self, filename: str, default_section: str = 'Default')`**  
  Initialise the configuration system with the given INI file and default section.

- **`__getitem__(self, section: str) -> Section`**  
  Retrieve a section using dictionary-style access. Creates the section if it does not exist.

- **`__getattr__(self, name: str) -> ConfigValue`**  
  Get a key from the default section using dot notation.

- **`__setattr__(self, name: str, value: str)`**  
  Set a key in the default section using dot notation.

- **`reload(self)`**  
  Reload the configuration file from disk.

- **`ensure_section(self, section: str)`**  
  Ensure that a section exists in the configuration.

- **`remove_key(self, section: str, key: str)`**  
  Remove a key from a specified section.

- **`remove_section(self, section: str)`**  
  Remove an entire section from the configuration.

- **`update_section(self, section: str, data: dict)`**  
  Batch update keys in a section using a dictionary.

### DynamicConfig.Section

- **`__getattr__(self, key: str) -> ConfigValue`**  
  Retrieve a key's value within this section using dot notation.

- **`__setattr__(self, key: str, value: str)`**  
  Set a key’s value within this section.

- **`__getitem__(self, key: str) -> ConfigValue`**  
  Retrieve a key's value within this section using dictionary-style access.

- **`__setitem__(self, key: str, value: str)`**  
  Set a key's value within this section using dictionary-style access.

- **`remove(self, key: str)`**  
  Remove a key from this section.

- **`keys(self) -> list`**  
  List all keys in this section.

### ConfigValue

- **`or_default(self, default_value: str, update: bool = False) -> str`**  
  Return the current value if non-empty; otherwise, return a default value. If `update` is set to True, update the configuration.

- **`as_int(self, default: int = 0) -> int`**  
  Convert the value to an integer, or return the specified default if conversion fails.

- **`as_float(self, default: float = 0.0) -> float`**  
  Convert the value to a float, or return the specified default if conversion fails.

- **`as_bool(self, default: bool = False) -> bool`**  
  Convert the value to a boolean, or return the specified default if conversion fails.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
