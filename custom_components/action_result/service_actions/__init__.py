"""Action handlers package for action_result.

This integration does not register any custom services.
Action responses are captured via the DataUpdateCoordinator by calling
existing Home Assistant services with return_response=True.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def async_setup_service_actions(hass: HomeAssistant) -> None:
    """
    Register service actions for the integration.

    Currently, this integration does not provide any custom services.
    The core functionality is to call existing HA services and expose
    their response data through sensor entities.
    """
    # No custom services registered for this integration
