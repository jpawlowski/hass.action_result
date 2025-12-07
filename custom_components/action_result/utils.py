"""Utility functions for action_result integration."""

from __future__ import annotations

import re
from typing import Any


def extract_data_at_path(data: Any, path: str | None) -> Any:
    """
    Extract data from a nested structure using a path with Jinja2-like syntax.

    Supports:
    - Dot notation: "forecast.0.temperature"
    - Bracket notation for keys with dots: ["weather.forecast_home"].forecast
    - Array indices: [0], [-1] (negative indices from end)
    - Mixed: ["weather.forecast_home"].forecast[0].temperature

    Args:
        data: The data structure to traverse.
        path: A path string using dots, brackets, or mixed notation.

    Examples:
              - "data.items"
              - ["weather.forecast_home"].forecast
              - items[0].temperature
              - ["key.with.dots"][0].value

    Returns:
        The data at the specified path, or the original data if path is empty/None.
    """
    if path is None or not path.strip():
        return data

    current = data
    path = path.strip()
    pos = 0

    while pos < len(path):
        # Skip leading dots
        if path[pos] == ".":
            pos += 1
            continue

        # Handle bracket notation: ["key"] or [0]
        if path[pos] == "[":
            end_bracket = path.find("]", pos)
            if end_bracket == -1:
                # Malformed bracket - return None
                return None

            bracket_content = path[pos + 1 : end_bracket]

            # Check if it's a quoted string: ["key"]
            if (bracket_content.startswith('"') and bracket_content.endswith('"')) or (
                bracket_content.startswith("'") and bracket_content.endswith("'")
            ):
                # Dictionary key with quotes
                key = bracket_content[1:-1]
                if isinstance(current, dict):
                    current = current.get(key)
                else:
                    return None
            else:
                # Array index: [0] or [-1]
                try:
                    index = int(bracket_content)
                    if isinstance(current, list):
                        if -len(current) <= index < len(current):
                            current = current[index]
                        else:
                            return None
                    else:
                        return None
                except ValueError:
                    # Invalid index
                    return None

            pos = end_bracket + 1
            if current is None:
                return None

        else:
            # Handle dot notation: extract key until next . or [
            match = re.match(r"([^.\[\]]+)", path[pos:])
            if not match:
                break

            key = match.group(1)

            # Try to use as array index first if current is a list
            if isinstance(current, list):
                try:
                    index = int(key)
                    if -len(current) <= index < len(current):
                        current = current[index]
                    else:
                        return None
                except ValueError:
                    # Not a valid index
                    return None
            elif isinstance(current, dict):
                current = current.get(key)
            else:
                # Cannot traverse further
                return None

            pos += len(key)
            if current is None:
                return None

    return current


def convert_to_bool(value: Any) -> bool | None:
    """
    Convert a value to boolean.

    Supports:
    - bool: True/False
    - int: 0=False, non-zero=True
    - str: "true"/"yes"/"on"/"1" = True, "false"/"no"/"off"/"0" = False (case-insensitive)
    - None: None (unavailable)

    Returns:
        Boolean value or None if conversion is not possible.
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return bool(value)

    if isinstance(value, str):
        value_lower = value.lower().strip()
        if value_lower in ("true", "yes", "on", "1"):
            return True
        if value_lower in ("false", "no", "off", "0"):
            return False

    # Cannot convert
    return None
