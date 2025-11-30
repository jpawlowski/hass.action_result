"""YAML validation and parsing for config flow service data."""

from __future__ import annotations

from typing import Any

import yaml


def validate_service_yaml(yaml_string: str) -> tuple[bool, str | None]:
    """
    Validate YAML string for service data.

    Args:
        yaml_string: The YAML string to validate.

    Returns:
        A tuple of (is_valid, error_key).
        If valid, returns (True, None).
        If invalid, returns (False, error_key) where error_key is a translation key.
    """
    if not yaml_string or not yaml_string.strip():
        return True, None

    try:
        parsed = yaml.safe_load(yaml_string)
        if parsed is not None and not isinstance(parsed, dict):
            return False, "yaml_not_dict"
    except yaml.YAMLError:
        return False, "yaml_parse_error"

    return True, None


def parse_service_yaml(
    yaml_string: str,
) -> tuple[dict[str, Any] | None, str | None, str | None, str | None]:
    """
    Parse YAML and extract service action, entry_id, and clean service data.

    This function handles the case where users paste full YAML from Developer Tools,
    e.g.:
        action: tibber_prices.get_chartdata
        data:
          entry_id: 01KAEWT06A1R2N0CA0YX9V2ZMK
          include_level: true

    It extracts:
    - The action (domain.service) if present
    - The entry_id if present in data
    - The cleaned data (without entry_id if it was extracted)

    Args:
        yaml_string: The YAML string to parse.

    Returns:
        A tuple of (cleaned_data_dict, action, entry_id, error_key).
        - cleaned_data_dict: Dict of service data (or None on error)
        - action: The action string like "domain.service" (or None)
        - entry_id: The entry_id if found (or None)
        - error_key: Translation key for any error (or None if valid)
    """
    if not yaml_string or not yaml_string.strip():
        return {}, None, None, None

    try:
        parsed = yaml.safe_load(yaml_string)
    except yaml.YAMLError:
        return None, None, None, "yaml_parse_error"

    if parsed is None:
        return {}, None, None, None

    if not isinstance(parsed, dict):
        return None, None, None, "yaml_not_dict"

    action: str | None = None
    entry_id: str | None = None
    cleaned_data: dict[str, Any] = {}

    # Check if this looks like full Developer Tools YAML
    if "action" in parsed or "service" in parsed:
        # Extract action (prefer "action" over "service" for modern syntax)
        action = parsed.get("action") or parsed.get("service")

        # Extract data section
        data_section = parsed.get("data", {})
        if isinstance(data_section, dict):
            cleaned_data = dict(data_section)
            # Extract entry_id if present
            if "entry_id" in cleaned_data:
                entry_id = cleaned_data.pop("entry_id")
        else:
            # data section is not a dict
            return None, action, None, "yaml_not_dict"
    else:
        # This is just plain service data
        cleaned_data = dict(parsed)
        # Extract entry_id if present at top level
        if "entry_id" in cleaned_data:
            entry_id = cleaned_data.pop("entry_id")

    return cleaned_data, action, entry_id, None


def dict_to_yaml(data: dict[str, Any]) -> str:
    """
    Convert a dictionary to YAML string.

    Args:
        data: The dictionary to convert.

    Returns:
        YAML string representation of the data.
    """
    if not data:
        return ""
    return yaml.dump(data, default_flow_style=False, allow_unicode=True).strip()


__all__ = ["dict_to_yaml", "parse_service_yaml", "validate_service_yaml"]
