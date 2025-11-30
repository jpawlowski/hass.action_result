"""
Config flow schemas.

Schemas for the main configuration flow steps:
- User setup (configure service to call)
- Reconfiguration
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.service_result.const import CONF_NAME, CONF_SERVICE_ACTION, CONF_SERVICE_DATA_YAML
from homeassistant.helpers import selector


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Get schema for user step (initial setup).

    The schema uses a service action selector (dropdown) for easy service selection.
    Users can optionally paste full YAML from Developer Tools; the system will
    auto-extract the action and data.

    Args:
        defaults: Optional dictionary of default values to pre-populate the form.

    Returns:
        Voluptuous schema for service configuration input.
    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=defaults.get(CONF_NAME, vol.UNDEFINED),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            vol.Optional(
                CONF_SERVICE_ACTION,
                default=defaults.get(CONF_SERVICE_ACTION, vol.UNDEFINED),
            ): selector.ActionSelector(),
            vol.Optional(
                CONF_SERVICE_DATA_YAML,
                default=defaults.get(CONF_SERVICE_DATA_YAML, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                    multiline=True,
                ),
            ),
        },
    )


def get_reconfigure_schema(current_data: Mapping[str, Any]) -> vol.Schema:
    """
    Get schema for reconfigure step.

    Args:
        current_data: Current configuration data to pre-fill in the form.

    Returns:
        Voluptuous schema for reconfiguration.
    """
    # Build action default from domain/name if present
    service_action = current_data.get(CONF_SERVICE_ACTION, {})
    if not service_action:
        # Backwards compatibility: build from old format
        domain = current_data.get("service_domain", "")
        name = current_data.get("service_name", "")
        if domain and name:
            service_action = {"action": f"{domain}.{name}"}

    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=current_data.get(CONF_NAME, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            vol.Optional(
                CONF_SERVICE_ACTION,
                default=service_action if service_action else vol.UNDEFINED,
            ): selector.ActionSelector(),
            vol.Optional(
                CONF_SERVICE_DATA_YAML,
                default=current_data.get(CONF_SERVICE_DATA_YAML, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                    multiline=True,
                ),
            ),
        },
    )


__all__ = [
    "get_reconfigure_schema",
    "get_user_schema",
]
