"""
bitdict module for creating and manipulating bit field dictionaries.

This module provides a `bitdict_factory` function that dynamically generates
classes for working with bit fields within an integer value.  These classes,
referred to as BitDicts, allow you to define a structure of named bit fields,
each with a specified start position, width, and data type.


- **Dynamic Bitfield Definition:**  Define bitfield layouts at runtime using
    a configuration dictionary.
- **Data Type Support:** Supports boolean, unsigned integer, and signed
    integer bitfields.
- **Nested BitDicts:** Allows defining hierarchical structures with nested
    BitDicts, selected by a selector property.
- **Data Validation:**  Performs validation of property configurations,
    including type checking and range validation.
- **Conversion Methods:** Provides methods for converting BitDicts to and
    from integers, bytes, and JSON-compatible dictionaries.

Usage:

1.  Define a configuration dictionary specifying the bitfield layout.
2.  Call `bitdict_factory` with the configuration to create a BitDict class.
3.  Instantiate the generated class to create a BitDict object.
4.  Access and manipulate bitfields using item access (e.g., `bd["field_name"]`).
"""

from __future__ import annotations
from typing import Any, Generator
from types import MappingProxyType
from copy import deepcopy


def _calculate_total_width(cfg) -> int:
    """
    Calculates the total bit width based on the configuration.

    This is a helper function that calculates the total number of bits
    required to store all the bit fields defined in the configuration.

    Args:
        cfg (dict): The configuration dictionary.

    Returns:
        int: The total bit width.
    """
    max_bit = 0
    for prop_config in cfg.values():
        end_bit = prop_config["start"] + prop_config["width"]
        max_bit = max(max_bit, end_bit)
    return max_bit


def _validate_property_config(
    prop_config_top: dict[str, Any], subtypes: dict[str, list[type | None]]
) -> None:
    """
    Recursively validates the property configuration.

    This helper function checks that the configuration dictionary
    is valid, including the nested configurations for 'bitdict' types.
    It ensures that all required keys are present, that property names
    are valid identifiers, that bit fields do not overlap, and that
    default values are within the allowed range for the data type.

    Args:
        prop_config_top (dict): The top-level configuration dictionary.

    Raises:
        ValueError: If the configuration is invalid.
        TypeError: If the config is not a dictionary.
    """
    for prop_name, prop_config in prop_config_top.items():
        _validate_basic_properties(prop_name, prop_config)
        _validate_default_values(prop_name, prop_config)
        _validate_valid_key(prop_name, prop_config)

        if prop_config["type"] == "bitdict":
            _validate_bitdict_properties(
                prop_name, prop_config, prop_config_top, subtypes
            )


def _validate_basic_properties(prop_name: str, prop_config: dict[str, Any]) -> None:
    """Validates the basic properties of a bitfield property configuration.

    Args:
        prop_name (str): The name of the property. Must be a valid identifier.
        prop_config (dict[str, Any]): A dictionary containing the property configuration.
            Must contain the keys "start", "width", and "type".

    Raises:
        ValueError: If the property name is not a valid identifier,
            if the property configuration is missing required keys,
            if the start value is not a non-negative integer,
            if the width value is not a positive integer,
            if the type value is not one of "bool", "uint", "int", "reserved", or "bitdict",
            or if the type is "bool" and the width is not 1.
        TypeError: If the property configuration is not a dictionary or MappingProxyType.
    """
    _validate_property_name(prop_name)
    _validate_config_type_and_keys(prop_config)
    _validate_start_and_width(prop_config)
    _validate_type(prop_config)
    _validate_valid_key(prop_name, prop_config)
    _validate_description(prop_config)


def _validate_description(prop_config: dict[str, Any]) -> None:
    """Validates the description key in the property configuration."""
    if "description" in prop_config and not isinstance(prop_config["description"], str):
        raise ValueError("Description must be a string")


def _validate_property_name(prop_name: str) -> None:
    """Validates that the property name is a valid identifier."""
    if not isinstance(prop_name, str) or not prop_name.isidentifier():
        raise ValueError(f"Invalid property name: {prop_name}")


def _validate_config_type_and_keys(prop_config: dict[str, Any]) -> None:
    """Validates the type and required keys of the property configuration."""
    required_keys = {"start", "width", "type"}
    if not isinstance(prop_config, (dict, MappingProxyType)):
        raise TypeError(
            "Property configuration must be a dictionary or MappingProxyType"
        )
    if not required_keys.issubset(prop_config):
        missing_keys = required_keys - set(prop_config)
        raise ValueError(f"Missing required keys in property config: {missing_keys}")


def _validate_start_and_width(prop_config: dict[str, Any]) -> None:
    """Validates the start and width values in the property configuration."""
    if not isinstance(prop_config["start"], int) or prop_config["start"] < 0:
        raise ValueError(f"Invalid start value: {prop_config['start']}")
    if not isinstance(prop_config["width"], int) or prop_config["width"] <= 0:
        raise ValueError(f"Invalid width value: {prop_config['width']}")


def _validate_type(prop_config: dict[str, Any]) -> None:
    """Validates the type value in the property configuration."""
    valid_types = {"bool", "uint", "int", "bitdict"}
    if prop_config["type"] not in valid_types:
        raise ValueError(f"Invalid type value: {prop_config['type']}")
    if prop_config["type"] == "bool" and prop_config["width"] != 1:
        raise ValueError("Boolean properties must have width 1")


def _validate_default_values(prop_name: str, prop_config: dict[str, Any]) -> None:
    """Validates and sets default values for properties in a bitfield configuration.

    This function checks if the provided default value for a property matches the
    expected type based on the property's configuration. If no default value is
    provided and the property type is 'bool', 'uint', or 'int', it assigns a
    default value of False, 0, or 0 respectively. It also validates that the
    default value for 'uint' and 'int' types falls within the allowed range
    defined by the property's width.

    Args:
        prop_name: The name of the property being validated (used for error messages).
        prop_config: A dictionary containing the configuration for the property,
            including its 'type', 'width' (for 'uint' and 'int'), and optionally
            'default' value.

    Raises:
        ValueError: If the property type is 'bitdict' and a default
            value is provided, or if the default value for 'uint' or 'int' is
            outside the allowed range.
        TypeError: If the default value does not match the expected type
            (bool for 'bool', int for 'uint' and 'int').
    """
    prop_type = prop_config["type"]
    if prop_type == "bitdict":
        if "default" in prop_config:
            raise ValueError("'bitdict' types cannot have a default values.")
        return

    if "default" not in prop_config:
        assert not isinstance(
            prop_config, MappingProxyType
        ), "Defaults not defined but config already frozen."
        _set_missing_defaults(prop_config)
        return

    if "description" not in prop_config:
        assert not isinstance(
            prop_config, MappingProxyType
        ), "Defaults not defined but config already frozen."
        prop_config["description"] = ""

    _validate_default_value_type(prop_name, prop_config)


def _set_missing_defaults(prop_config: dict[str, Any]) -> None:
    """Sets default values if they are missing in the property configuration."""
    prop_type = prop_config["type"]
    if prop_type == "bool":
        prop_config["default"] = False
    elif prop_type in ("uint", "int"):
        prop_config["default"] = 0


def _validate_default_value_type(prop_name: str, prop_config: dict[str, Any]) -> None:
    """Validates the type and range of the default value."""
    default_value = prop_config["default"]
    prop_type = prop_config["type"]
    width = prop_config["width"]

    if prop_type == "bool":
        if not isinstance(default_value, bool):
            raise TypeError(
                f"Invalid default type for property {prop_name}"
                f" expecting bool: {type(default_value)}"
            )
    elif prop_type in ("uint", "int"):
        if not isinstance(default_value, int):
            raise TypeError(
                f"Invalid default type for property {prop_name}"
                f" expecting int: {type(default_value)}"
            )
        if prop_type == "uint":
            if not 0 <= default_value < (1 << width):
                raise ValueError(
                    f"Invalid default value for property"
                    f" {prop_name}: {default_value}"
                )
        else:  # prop_type == "int"
            if not -(1 << (width - 1)) <= default_value < (1 << (width - 1)):
                raise ValueError(
                    f"Invalid default value for property {prop_name}"
                    f": {default_value}"
                )


def _validate_bitdict_properties(
    prop_name: str,
    prop_config: dict[str, Any],
    prop_config_top: dict[str, Any],
    subtypes: dict[str, list[type | None]],
) -> None:
    """Validates the properties of a 'bitdict' type configuration.

    This function checks if the provided configuration for a 'bitdict' type property
    is valid. It verifies the existence and type of required fields like 'subtype'
    (a list) and 'selector' (a string). It also validates the selector property
    itself, ensuring it exists in the top-level configuration, is of type 'bool' or
    'uint', and has a width no greater than 16.  It also establishes a reverse
    linkage from the selector property to the bitdict property name. Finally, it
    recursively validates the configurations of the subtypes.

    Args:
        prop_name: The name of the property being validated.
        prop_config: The configuration dictionary for the 'bitdict' property.
        prop_config_top: The top-level configuration dictionary containing all properties.
        subtypes: A dictionary to store the validated subtypes.  The keys are the
            property names and the values are lists of types (or None).

    Raises:
        ValueError: If any of the following conditions are met:
            - 'subtype' is missing or not a list.
            - 'selector' is missing or not a string.
            - The selector property does not exist in the top-level configuration.
            - The selector property is not of type 'bool' or 'uint'.
            - The selector property's width is greater than 16.
            - The 'subtype' list is empty.
    """
    if "subtype" not in prop_config or not isinstance(prop_config["subtype"], list):
        raise ValueError("'bitdict' type requires a 'subtype' list")
    if "selector" not in prop_config or not isinstance(prop_config["selector"], str):
        raise ValueError("'bitdict' type requires a 'selector' field")
    selector = prop_config["selector"]
    if selector not in prop_config_top:
        raise ValueError(f"Invalid selector property: {selector}")
    if prop_config_top[selector]["type"] not in (
        "bool",
        "uint",
    ):
        raise ValueError("Selector property must be of type 'bool' or 'uint'")
    if prop_config_top[selector]["width"] > 16:
        raise ValueError("Selector property width must be <= 16 (65536 subtypes)")

    # Reverse linkage
    prop_config_top[selector]["_bitdict"] = prop_name

    if len(prop_config["subtype"]) == 0:
        raise ValueError(
            f"'bitdict' type for property '{prop_name}' must have at least one subtype"
        )

    for idx, sub_config in enumerate(prop_config["subtype"]):
        # Recursively validate sub-configurations
        subtypes.setdefault(prop_name, []).append(
            None
            if sub_config is None
            else bitdict_factory(
                sub_config,
                name=f"prop_name{idx}",
                title=f"{prop_name}: {selector} = {idx}",
            )
        )  # We can use the factory recursively
        if sub_config is None and _is_valid_value(idx, prop_config_top[selector]):
            raise ValueError(
                f"Subtype {idx} for property '{prop_name}' "
                "is a valid selection but no bitdict defined."
            )


def _validate_valid_key(prop_name: str, prop_config: dict[str, Any]) -> None:
    """Validates the 'valid' key in the property configuration."""
    if prop_config["type"] == "bitdict":
        if "valid" in prop_config:
            raise ValueError(f"'valid' key not allowed for {prop_config['type']} type")
        return

    if "valid" not in prop_config:
        return

    valid_config = prop_config["valid"]
    if not isinstance(valid_config, dict):
        raise ValueError(f"'valid' must be a dictionary for property {prop_name}")

    if not valid_config:
        raise ValueError(f"'valid' dictionary cannot be empty for property {prop_name}")

    if "value" not in valid_config and "range" not in valid_config:
        raise ValueError(
            f"'valid' dictionary must contain 'value' or 'range' for property {prop_name}"
        )

    _validate_valid_value(prop_name, prop_config, valid_config)
    _validate_valid_range(prop_name, prop_config, valid_config)


def _validate_valid_value(
    prop_name: str, prop_config: dict[str, Any], valid_config: dict[str, Any]
) -> None:
    """Validates the 'value' key within the 'valid' configuration."""
    if "value" not in valid_config:
        return

    if not isinstance(valid_config["value"], set):
        raise ValueError(
            f"'value' in 'valid' dictionary must be a set for property {prop_name}"
        )
    if not valid_config["value"]:
        raise ValueError(
            f"'value' set in 'valid' dictionary cannot be empty for property {prop_name}"
        )
    for val in valid_config["value"]:
        if not isinstance(val, (int, bool)):
            raise ValueError(
                f"Invalid value type in 'valid' set for property {prop_name}: {val}"
            )
        if not _is_value_in_range(val, prop_config):
            raise ValueError(f"Value {val} out of range for property {prop_name}")


def _validate_valid_range(
    prop_name: str, prop_config: dict[str, Any], valid_config: dict[str, Any]
) -> None:
    """Validates the 'range' key within the 'valid' configuration."""
    if "range" not in valid_config:
        return

    if not isinstance(valid_config["range"], list):
        raise ValueError(
            f"'range' in 'valid' dictionary must be a list for property {prop_name}"
        )
    if not valid_config["range"]:
        raise ValueError(
            f"'range' list in 'valid' dictionary cannot be empty for property {prop_name}"
        )
    for r in valid_config["range"]:
        if not isinstance(r, tuple) or not 1 <= len(r) <= 3:
            raise ValueError(
                f"Invalid range tuple in 'valid' list for property {prop_name}: {r}"
            )
        for val in range(*r):
            if not _is_value_in_range(val, prop_config):
                raise ValueError(f"Value {val} out of range for property {prop_name}")


def _is_valid_value(value: int | bool, prop_config: dict[str, Any]) -> bool:
    """Checks if a value is valid according to the 'valid'
    key in the property configuration."""
    if "valid" not in prop_config:
        return True

    valid_config = prop_config["valid"]
    if "value" in valid_config and value in valid_config["value"]:
        return True

    if "range" in valid_config:
        for r in valid_config["range"]:
            if value in range(*r):
                return True

    return False


def _is_value_in_range(value: int | bool, prop_config: dict[str, Any]) -> bool:
    """Checks if a value is within the allowed range for a property."""
    if prop_config["type"] == "bool":
        return value in (True, False)
    width = prop_config["width"]
    if prop_config["type"] == "uint":
        return 0 <= value < (1 << width)
    assert prop_config["type"] == "int", "Unexpected property type"
    return -(1 << (width - 1)) <= value < (1 << (width - 1))


def _check_overlapping(cfg) -> None:
    """
    Checks for overlapping bit field definitions.

    This helper function ensures that no two bit fields in the
    configuration overlap.

    Args:
        cfg (dict): The configuration dictionary.

    Raises:
        ValueError: If any bit fields overlap.
    """
    used_bits = set()
    for _, prop_config in cfg.items():
        for i in range(
            prop_config["start"], prop_config["start"] + prop_config["width"]
        ):
            if i in used_bits:
                raise ValueError(
                    f"Overlapping bit definitions: bit {i} is used by multiple properties"
                )
            used_bits.add(i)


def bitdict_factory(  # pylint: disable=too-many-statements
    config: dict[str, Any], name: str = "BitDict", title: str = "BitDict"
) -> type:
    """
    Factory function to create BitDict classes based on a configuration.

    This factory function dynamically creates a new class (subclass of BitDict)
    based on the provided configuration dictionary. The generated class allows
    you to define and access bit fields within an integer value, similar to
    a struct in C.

    Args:
        config (dict): A dictionary defining the bit field structure.
            The dictionary keys are the names of the bit fields, and the values
            are dictionaries with the following keys:

            * `start` (int): The starting bit position (LSB = 0).
            * `width` (int): The width of the bit field in bits.
            * `type` (str): The data type of the bit field.
              Can be one of: 'bool', 'uint', 'int', 'reserved', 'bitdict'.
            * `default` (optional): The default value for the bit field.
              If not provided, defaults to False for 'bool', 0 for 'uint' and 'int'.
            * `subtype` (list of dict, optional):  Required for 'bitdict' type.
              Ignored for other types.
              A list of sub-bitdict configurations to select from based
              on the value of the selector property.
            * `selector` (str, optional): Required for 'bitdict' type.
              Ignored for other types
              The name of the property used to select the active sub-bitdict.
              This property must be of type 'bool' or 'uint' and have a width <= 16.

        name (str, optional): The name of the generated class.
            Defaults to "BitDict". Must be a valid python identifier.
        title (str, optional): The title of the generated class. Used in generating
            the markdown documentation with `config_to_markdown`. Defaults to "BitDict".

    Returns:
        type: A new class that represents the bit field structure.

    Raises:
        ValueError: If the configuration is invalid (e.g., overlapping
            bit fields, invalid property names, missing required keys).
        TypeError: If the config is not a dictionary.

    Example:
        ```python
        config = {
            'enabled': {'start': 0, 'width': 1, 'type': 'bool'},
            'mode': {'start': 1, 'width': 2, 'type': 'uint'},
            'value': {'start': 3, 'width': 5, 'type': 'int'},
        }
        MyBitDict = bitdict_factory(config, "MyBitDict")

        # Create an instance of the generated class
        bd = MyBitDict()

        # Set and access bit fields
        bd['enabled'] = True
        bd['mode'] = 2
        bd['value'] = -5

        # Get the integer representation
        value = bd.to_int()

        # Create an instance from an integer
        bd2 = MyBitDict(value)
        ```
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    if not name.isidentifier():
        raise ValueError("Invalid class name")

    # Subtype classes are stored in a dictionary for recursive creation.
    subtype_lists: dict[str, list[type | None]] = {}
    _title: str = title

    _validate_property_config(config, subtype_lists)  # Initial validation of top level.
    _check_overlapping(config)
    total_width = _calculate_total_width(config)

    class BitDict:
        """
        A dynamic bit-field dictionary for structured data manipulation.

        BitDict provides a flexible way to define and interact with data structures
        where individual fields occupy specific bit ranges. It supports a variety of
        data types including integers (signed and unsigned), booleans, and nested
        BitDict instances, enabling complex data layouts to be easily managed.

        Key Features:
        - **Dynamic Configuration:**  BitDict classes are dynamically created based on a
          provided configuration, defining the structure and properties of the bit field.
        - **Sub-BitDict Support:** Allows nesting of BitDict instances, enabling hierarchical
          data structures with conditional sub-fields based on selector values.
        - **Type Handling:** Enforces type and range checking for property assignments,
          ensuring data integrity.
        - **Data Conversion:** Supports conversion to and from integers, bytes, and
          JSON-compatible dictionaries.
        - **Iteration:** Provides an iterator to traverse properties in LSB to MSB order.

        Use Cases:
        - Parsing and generating binary data formats (e.g., network packets, file formats).
        - Representing hardware registers and memory-mapped I/O.
        - Implementing data structures with specific bit-level packing requirements.

        Example:
        ```python
        config = {
            "enabled": {"type": "bool", "start": 0, "width": 1, "default": False},
            "mode": {"type": "uint", "start": 1, "width": 2, "default": 0},
            "value": {"type": "int", "start": 3, "width": 5, "default": 0},
        }
        MyBitDict = bitdict_factory("MyBitDict", config)
        my_dict = MyBitDict()
        my_dict["enabled"] = True
        my_dict["mode"] = 2
        my_dict["value"] = -5
        print(my_dict.to_json())
        ```
        """

        _config: MappingProxyType[str, Any] = MappingProxyType(deepcopy(config))
        subtypes: dict[str, list[type | None]] = subtype_lists
        _total_width: int = total_width
        title: str = _title
        __name__: str = name

        def __init__(
            self, value: int | bytes | bytearray | dict[str, Any] | None = None
        ) -> None:
            """Initializes a BitDict instance with a specified value.
            The initial value can be provided as an integer,
            bytes/bytearray, or a dictionary. If no value is provided,
            the BitDict is initialized to its default state (all bits
            zeroed).

                value (int | bytes | bytearray | dict[str, Any] | None,
                optional): The initial value for the BitDict.
                    - If `int`, the BitDict is set to this integer value.
                      Value must be within the representable range.
                    - If `bytes` or `bytearray`, the BitDict is initialized
                      from the big-endian representation of these bytes. The
                      length of the byte sequence must be appropriate for the
                      BitDict's total width.
                    - If `dict`, the BitDict is initialized using the
                      dictionary's key-value pairs.
                    - If `None`, the BitDict is initialized to its default
                      state. Defaults to None.

                TypeError: If `value` is not one of the supported types
                    (int, bytes, bytearray, dict, None).
                ValueError:
                    - If `value` is an integer that exceeds the maximum or
                      falls below the minimum representable value given the
                      BitDict's total width.
                    - If `value` is a bytes or bytearray object whose length
                      is incompatible with the BitDict's total width.
            """
            self._value = 0
            # Instances of subbitdicts
            self._subbitdicts: dict[str, list[BitDict | None]] = {}

            # Identification of this BitDict in a parent BitDict
            # These are set by _parent_config() when this BitDict is a sub-bitdict.
            # They are used in _update_parent() to update the parent BitDict
            # when this BitDict changes.
            self._parent: BitDict | None = None
            self._parent_key: str | None = None

            # Set to defaults
            if value is None:
                self.reset()
            elif isinstance(value, int):
                if value >= (1 << self._total_width):
                    raise ValueError(
                        f"Integer value {value} exceeds maximum"
                        f" value for bit width {self._total_width}"
                    )
                if value < -(1 << (self._total_width - 1)):
                    raise ValueError(
                        f"Integer value {value} exceeds minimum"
                        f"value for bit width {self._total_width}"
                    )
                self.set(value)
            elif isinstance(value, (bytes, bytearray)):
                if len(value) > (self._total_width + 7) // 8:  # +7 to round up
                    raise ValueError(
                        f"Bytes object too long for bit width {self._total_width}"
                    )
                # Convert bytes to integer (big-endian)
                self.set(int.from_bytes(value, "big"))
            elif isinstance(value, dict):
                self.set(value)  # Use update to handle defaults and type checking
            else:
                raise TypeError(
                    "Invalid initialization type: must be None, int, bytes, bytearray, or dict"
                )

        def __getitem__(self, key: str) -> bool | int | BitDict:
            """
            Retrieves the value associated with the given key.
            The key corresponds to a property defined in the BitDict's configuration.
            The type of the returned value depends on the property's type:
            - 'bool': Returns a boolean value.
            - 'int': Returns a signed integer value (two's complement).
            - 'uint': Returns an unsigned integer value.
            - 'bitdict': Returns a sub-BitDict, selected by the value of another property.
            Args:
                key: The name of the property to retrieve.
            Returns:
                The value of the property, with the type depending on the property's configuration.
                Can be a bool, int, or BitDict.
            Raises:
                KeyError: If the key is not a valid property in the configuration.
                ValueError: If attempting to read a 'reserved' property.
                AssertionError: If the selector value for a 'bitdict' type is not an integer,
                        or if an unknown property type is encountered.
            """
            if key not in self._config:
                raise KeyError(f"Invalid property: {key}")

            prop_config = self._config[key]
            start = prop_config["start"]
            width = prop_config["width"]
            mask = (1 << width) - 1
            raw_value = (self._value >> start) & mask

            if prop_config["type"] == "bool":
                return bool(raw_value)

            if prop_config["type"] == "uint":
                return raw_value

            if prop_config["type"] == "int":
                # Two's complement conversion if the highest bit is set
                return (
                    raw_value - (1 << width)
                    if raw_value & (1 << (width - 1))
                    else raw_value
                )

            if prop_config["type"] == "bitdict":
                selector_value: bool | int | BitDict = self[prop_config["selector"]]
                assert isinstance(selector_value, int), "Selector must be an integer"
                bd: BitDict = self._get_subbitdict(key, selector_value)
                return bd

            assert False, f"Unknown property type: {prop_config['type']}"

        def __setitem__(self, key: str, value: bool | int) -> None:
            """Sets the value of a property within the BitDict.
            Args:
                key (str): The name of the property to set.
                value (bool | int): The value to set the property to.  Must be
                a boolean or integer, depending on the property's type.
            Raises:
                KeyError: If the given key is not a valid property in the BitDict's configuration.
                ValueError: If attempting to set a reserved property, or if the provided value
                is out of the allowed range for the property.
                TypeError: If the provided value is not of the expected type (boolean or integer)
                for the property.
            """
            if key not in self._config:
                raise KeyError(f"Invalid property: {key}")

            prop_config = self._config[key]
            start = prop_config["start"]
            width = prop_config["width"]
            mask = (1 << width) - 1

            match prop_config["type"]:
                case "bool":
                    if not isinstance(value, (bool, int)):
                        raise TypeError(
                            f"Expected boolean or integer value for property '{key}'"
                        )
                    value = 1 if value else 0
                case "uint":
                    if not isinstance(value, int):
                        raise TypeError(f"Expected integer value for property '{key}'")
                    if not 0 <= value < (1 << width):
                        raise ValueError(
                            f"Value {value} out of range for property '{key}'"
                        )
                case "int":
                    if not isinstance(value, int):
                        raise TypeError(f"Expected integer value for property '{key}'")
                    if not -(1 << (width - 1)) <= value < (1 << (width - 1)):
                        raise ValueError(
                            f"Value {value} out of range for property '{key}'"
                        )
                    # Convert to two's complement representation
                    if value < 0:
                        value = (1 << width) + value
                case "bitdict":
                    # Set the sub-bitdict value.
                    selector_value = self[prop_config["selector"]]
                    assert isinstance(
                        selector_value, int
                    ), "Selector must be an integer"
                    bd: BitDict = self._get_subbitdict(key, selector_value)
                    bd.set(value)
                    value = bd.to_int()
                case _:
                    assert False, f"Unknown property type: {prop_config['type']}"

            # If the property is a selector then the sub-bitdict
            # changes and we need to update the value
            # Note that if the newly selected BitDict was previously
            # defined then that value will be used
            # or else it will be the default for the new BitDict.
            # It will not maintain the same numeric value.
            # This is important to call out in the user documentation.
            if "_bitdict" in prop_config:
                bd = self._get_subbitdict(prop_config["_bitdict"], value)
                bdc = self._config[prop_config["_bitdict"]]
                _mask = (1 << bdc["width"]) - 1
                _start = bdc["start"]
                self._value &= ~(_mask << _start)
                self._value |= (bd.to_int() & _mask) << _start

            # Clear the bits for this property, then set the new value
            self._value &= ~(mask << start)
            self._value |= (value & mask) << start

            # If this BitDict is a sub-bitdict then update the parent
            if self._parent is not None:
                self._update_parent()

        def __len__(self) -> int:
            """
            Returns the total width of the bit dictionary, representing the number
            of bits it can store.
            Returns:
                int: The total width (number of bits) of the bit dictionary.
            """

            return self._total_width

        def __contains__(self, key: str) -> bool:
            """Check if a property exists within this BitDict or its nested BitDicts.
            This method checks for the existence of a given key in the BitDict's configuration.
            It considers the current selector state, meaning that if a property exists only within
            a deselected subtype, this method will return False.
            Args:
                key: The property name (key) to check for.
            Returns:
                True if the property exists and is accessible given the current selector state,
                False otherwise.
            """
            retval: bool = key in self._config
            if not retval:
                for k, bd in self._config.items():
                    if bd["type"] == "bitdict":
                        bdi: bool | int | BitDict = self[k]
                        assert not isinstance(bdi, int), "Expecting BitDict type."
                        retval = retval or key in bdi
                        if retval:
                            break
            return retval

        def __iter__(self) -> Generator[tuple[str, bool | BitDict | int], Any, None]:
            """Iterates over the BitDict, yielding (name, value) pairs for each
            non-reserved field.
            Yields:
                Generator[tuple[Any, bool | Any | BitDict | None], Any, None]:
                A generator that yields tuples of (name, value), where name is the
                field name and value is the corresponding value in the BitDict.
                The values can be of type bool, Any, BitDict, or None.
            """
            sps = sorted(self._config.items(), key=lambda item: item[1]["start"])
            for name, _ in sps:
                yield name, self[name]

        def __repr__(self) -> str:
            """
            Return a string representation of the BitDict object.
            The string representation includes the class name and a JSON-like
            representation of the BitDict's contents, obtained via the `to_json()` method.
            Returns:
                str: A string representation of the BitDict.
            """

            return f"{self.__class__.__name__}({self.to_json()})"

        def __str__(self) -> str:
            """
            Returns a string representation of the BitDict object.

            This method converts the BitDict object to its JSON representation
            and then returns the string representation of that JSON object.

            Returns:
                str: A string representation of the BitDict object in JSON format.
            """

            return str(self.to_json())

        def _get_subbitdict(self, key: str, selector_value: int) -> BitDict:
            """Retrieves a sub-BitDict associated with a given key and selector value.
            If the sub-BitDict does not already exist, it is created, initialized,
            and stored for future access.
            Args:
                key: The key associated with the sub-BitDict.  This corresponds to a
                 property defined in the BitDict's configuration.
                selector_value: The selector value used to identify the specific
                        sub-BitDict within the list of possible sub-BitDicts
                        for the given key.  This value is typically derived
                        from another property acting as a selector.
            Returns:
                The sub-BitDict associated with the given key and selector value.
                The returned BitDict is guaranteed to exist.
            Raises:
                AssertionError: If the subtype class has not been created for the
                        given selector value, or if the created sub-BitDict
                        is None.
            """

            prop_config = self._config[key]
            if key not in self._subbitdicts:
                width = self._config[prop_config["selector"]]["width"]
                self._subbitdicts[key] = [None] * 2**width
            sdk: list[BitDict | None] = self._subbitdicts[key]
            if sdk[selector_value] is None:
                if selector_value >= len(self.subtypes[key]):
                    raise IndexError(
                        "Subtype class not created for selector"
                        f" {prop_config['selector']} at index {selector_value}"
                    )
                bdtype: type[BitDict] | None = self.subtypes[key][selector_value]
                assert bdtype is not None, "Subtype class not created!"
                nbd = bdtype()
                nbd._set_parent(self, key)  # pylint: disable=protected-access
                sdk[selector_value] = nbd
            retval: BitDict | None = sdk[selector_value]
            assert retval is not None, "Subtype class not created!"
            return retval

        def _set_parent(self, parent: BitDict, key: str) -> None:
            """Sets the parent BitDict and the key associated with this BitDict in the parent.
            Args:
                parent: The parent BitDict.
                key: The key associated with this BitDict in the parent.
            """

            self._parent = parent
            self._parent_key = key

        def _update_parent(self) -> None:
            """Updates the parent BitField with the current value of this BitField.
            This method assumes that the parent BitField, as well as the key
            associated with this BitField within the parent's configuration,
            are properly set. It calculates a mask based on the width defined
            in the parent's configuration for this BitField, clears the
            corresponding bits in the parent's value, and then sets those bits
            to the current value of this BitField.
            """

            assert self._parent is not None, "Parent not set"
            assert self._parent_key is not None, "Parent key not set"
            pc = self._parent._config[  # pylint: disable=protected-access
                self._parent_key
            ]
            mask = (1 << pc["width"]) - 1
            start = pc["start"]
            self._parent._value &= ~(mask << start)
            self._parent._value |= (self.to_int() & mask) << start

        def clear(self) -> None:
            """Clears the bit dictionary, setting all bits to 0."""

            self.set(0)

        def reset(self) -> None:
            """Resets the BitDict to its default values.
            Iterates through the properties defined in the configuration.
            If a property is a reserved type, it is skipped.
            If a property is a nested BitDict, its reset method is called recursively.
            Otherwise, the property is set to its default value as specified in the configuration.
            """

            for prop_name, prop_config in self._config.items():
                if prop_config["type"] == "bitdict":
                    selector_value = self[prop_config["selector"]]
                    assert isinstance(
                        selector_value, int
                    ), "Selector must be an integer"
                    self._get_subbitdict(prop_name, selector_value).reset()
                else:
                    self[prop_name] = prop_config["default"]

        def set(self, value: int | dict[str, Any]) -> None:
            """Sets the value of the BitDict.
            The value can be set in two ways:
            1.  As an integer: In this case, the integer value is assigned to the
                underlying integer representation of the BitDict.  A ValueError is
                raised if the integer is outside the allowed range, given the
                configured bit width. Note the integer must be >= 0.
            2.  As a dictionary: In this case, the dictionary is treated as a set
                of property values to be assigned to the BitDict.  The keys of the
                dictionary correspond to the property names defined in the BitDict's
                configuration.  If a property is present in the dictionary, its
                value is assigned to the corresponding sub-BitDict or bit field.
                If a property is not present in the dictionary but has a "default"
                value specified in the configuration, the default value is assigned.
            Args:
                value: The value to set.  Can be an integer or a dictionary of
                property values.
            Raises:
                ValueError: If the integer value is outside the allowed range for
                the configured bit width.
                AssertionError: If the selector value is not an integer when setting
                a sub-BitDict.
            """

            if isinstance(value, dict):
                for prop_name, prop_config in self._config.items():
                    if prop_name in value:
                        self[prop_name] = value[prop_name]
                    elif "default" in prop_config:
                        self[prop_name] = prop_config["default"]
            else:
                if value >= (1 << self._total_width):
                    raise ValueError(
                        f"Integer value {value} exceeds maximum"
                        f" value for bit width {self._total_width}"
                    )
                if value < 0:
                    raise ValueError(f"Integer must be non-negative, got {value}")
                self._value: int = value

                # Must set sub-bitdicts after setting the main value.
                for prop_name, prop_config in self._config.items():
                    if prop_config["type"] == "bitdict":
                        selector_value = self[prop_config["selector"]]
                        assert isinstance(
                            selector_value, int
                        ), "Selector must be an integer"
                        bd_value = (value >> prop_config["start"]) & (
                            (1 << prop_config["width"]) - 1
                        )
                        self._get_subbitdict(prop_name, selector_value).set(bd_value)

        def update(self, data: dict[str, Any]) -> None:
            """Update the BitDict with values from another dictionary.
            Args:
                data (dict[str, Any]): A dictionary containing the keys and values to update
                in the BitDict.  Keys must be strings and values must be convertible
                to integers within the BitDict's bit_length.
            Raises:
                TypeError: If `data` is not a dictionary.
                ValueError: If a value in `data` cannot be represented within the
                BitDict's bit_length.
            """

            if not isinstance(data, dict):
                raise TypeError("update() requires a dictionary")
            for key, value in data.items():
                self[key] = value  # Use __setitem__ for type/range checking

        def to_json(self) -> dict[str, Any]:
            """
            Converts the BitDict to a JSON-serializable dictionary.
            Iterates through the BitDict in reverse order, creating a dictionary
            where keys are the names of the bitfields and values are their
            corresponding values. If a value is a BitDict itself, its `to_json`
            method is called recursively to convert it to a JSON-serializable
            dictionary as well.
            Returns:
                dict[str, Any]: A dictionary representation of the BitDict suitable
                for JSON serialization.
            """

            result = {}
            for name, _ in list(self)[::-1]:  # Use the iterator
                result[name] = self[name]
                if hasattr(result[name], "to_json"):
                    result[name] = result[
                        name
                    ].to_json()  # Recurse for nested bitdicts.
            return result

        def to_bytes(self) -> bytes:
            """Convert the bit dictionary to a byte string.
            The resulting byte string represents the underlying integer value
            of the bit dictionary in big-endian byte order. The length of the
            byte string is determined by the total width of the bit dictionary,
            rounded up to the nearest whole byte.
            Returns:
                bytes: A byte string representing the bit dictionary's value.
            """

            num_bytes = (self._total_width + 7) // 8  # Round up to nearest byte
            return self._value.to_bytes(num_bytes, "big")

        def to_int(self) -> int:
            """
            Returns the integer representation of the BitDict.
            This method provides a way to access the underlying integer value
            that represents the BitDict's data.
            Returns:
                int: The integer value of the BitDict.
            """

            return self._value

        def valid(self) -> bool:
            """Checks if all properties have valid values."""
            for prop_name, prop_config in self._config.items():
                if prop_config["type"] == "bitdict":
                    selector_value = self[prop_config["selector"]]
                    assert isinstance(
                        selector_value, int
                    ), "Selector must be an integer"
                    if not _is_valid_value(
                        selector_value, self._config[prop_config["selector"]]
                    ):
                        return False
                    sub_bitdict = self._get_subbitdict(prop_name, selector_value)
                    if not sub_bitdict.valid():
                        return False
                else:

                    value = self[prop_name]
                    assert isinstance(
                        value, (int, bool)
                    ), "Value must be an integer or boolean"
                    if not _is_valid_value(value, prop_config):
                        return False
            return True

        def inspect(self) -> dict[str, dict[str, bool | int | dict]]:
            """Inspects the BitDict and returns a dictionary of properties with invalid values."""
            invalid_props = {}
            for prop_name, prop_config in self._config.items():
                if prop_config["type"] == "bitdict":
                    selector_value = self[prop_config["selector"]]
                    assert isinstance(
                        selector_value, int
                    ), "Selector must be an integer"
                    if not _is_valid_value(
                        selector_value, self._config[prop_config["selector"]]
                    ):
                        invalid_props[prop_config["selector"]] = selector_value
                    else:
                        sub_bitdict = self._get_subbitdict(prop_name, selector_value)
                        sub_invalid_props = sub_bitdict.inspect()
                        if sub_invalid_props:
                            invalid_props[prop_name] = sub_invalid_props
                else:
                    value = self[prop_name]
                    assert isinstance(
                        value, (int, bool)
                    ), "Value must be an integer or boolean"
                    if not _is_valid_value(value, prop_config):
                        invalid_props[prop_name] = self[prop_name]
            return invalid_props

        @classmethod
        def get_config(cls) -> MappingProxyType[str, Any]:
            """Returns the configuration settings for the BitDict class.
            The configuration is stored in a MappingProxyType, which provides
            a read-only view of the underlying dictionary. This prevents
            accidental modification of the configuration after the class
            has been initialized.
            Returns:
                MappingProxyType[str, Any]: A read-only mapping containing the
                configuration settings.
            """

            return cls._config

    # end class BitDict

    # Set the name of the dynamically created class.
    BitDict.__name__ = name
    return BitDict
