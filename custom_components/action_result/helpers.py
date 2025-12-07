"""Helper functions for extracting Home Assistant enums."""

from __future__ import annotations

import re
from typing import Any

from custom_components.action_result.const import (
    VALUE_TYPE_BOOLEAN,
    VALUE_TYPE_NUMBER,
    VALUE_TYPE_STRING,
    VALUE_TYPE_TIMESTAMP,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    CURRENCY_CENT,
    CURRENCY_DOLLAR,
    CURRENCY_EURO,
    PERCENTAGE,
    UnitOfApparentPower,
    UnitOfArea,
    UnitOfBloodGlucoseConcentration,
    UnitOfConductivity,
    UnitOfDataRate,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfEnergyDistance,
    UnitOfFrequency,
    UnitOfInformation,
    UnitOfIrradiance,
    UnitOfLength,
    UnitOfMass,
    UnitOfPower,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfReactiveEnergy,
    UnitOfReactivePower,
    UnitOfSoundPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
    UnitOfVolumetricFlux,
)


def get_all_sensor_device_classes() -> list[str]:
    """
    Get all available sensor device classes from Home Assistant.

    Returns:
        Sorted list of device class values.
    """
    return sorted([dc.value for dc in SensorDeviceClass])


def get_base_units_of_measurement() -> list[str]:
    """
    Get all base (non-composite) units of measurement from Home Assistant.

    Base units do not contain '/' or '⋅' characters and can be used
    to build custom composite units.

    Returns:
        Sorted list of unique base unit values.
    """
    unit_classes = [
        UnitOfApparentPower,
        UnitOfArea,
        UnitOfBloodGlucoseConcentration,
        UnitOfConductivity,
        UnitOfDataRate,
        UnitOfElectricCurrent,
        UnitOfElectricPotential,
        UnitOfEnergy,
        UnitOfEnergyDistance,
        UnitOfFrequency,
        UnitOfInformation,
        UnitOfIrradiance,
        UnitOfLength,
        UnitOfMass,
        UnitOfPower,
        UnitOfPrecipitationDepth,
        UnitOfPressure,
        UnitOfReactiveEnergy,
        UnitOfReactivePower,
        UnitOfSoundPressure,
        UnitOfSpeed,
        UnitOfTemperature,
        UnitOfTime,
        UnitOfVolume,
        UnitOfVolumeFlowRate,
        UnitOfVolumetricFlux,
    ]

    units = []
    # Extract all values from UnitOf* enums, but only base units (no composites)
    for unit_class in unit_classes:
        units.extend(unit.value for unit in unit_class if "/" not in unit.value and "⋅" not in unit.value)

    # Add percentage and currency symbols
    units.extend([PERCENTAGE, CURRENCY_EURO, CURRENCY_DOLLAR, CURRENCY_CENT])

    return sorted(set(units))


def get_all_units_of_measurement() -> list[str]:
    """
    Get all available units of measurement from Home Assistant.

    This dynamically extracts all units from Home Assistant's const module,
    including all UnitOf* classes, percentage, currency symbols, and
    common composite units like energy prices.

    Returns:
        Sorted list of unique unit values.
    """
    unit_classes = [
        UnitOfApparentPower,
        UnitOfArea,
        UnitOfBloodGlucoseConcentration,
        UnitOfConductivity,
        UnitOfDataRate,
        UnitOfElectricCurrent,
        UnitOfElectricPotential,
        UnitOfEnergy,
        UnitOfEnergyDistance,
        UnitOfFrequency,
        UnitOfInformation,
        UnitOfIrradiance,
        UnitOfLength,
        UnitOfMass,
        UnitOfPower,
        UnitOfPrecipitationDepth,
        UnitOfPressure,
        UnitOfReactiveEnergy,
        UnitOfReactivePower,
        UnitOfSoundPressure,
        UnitOfSpeed,
        UnitOfTemperature,
        UnitOfTime,
        UnitOfVolume,
        UnitOfVolumeFlowRate,
        UnitOfVolumetricFlux,
    ]

    units = []
    # Extract all values from UnitOf* enums
    for unit_class in unit_classes:
        units.extend([unit.value for unit in unit_class])

    # Add percentage and currency symbols
    units.extend([PERCENTAGE, CURRENCY_EURO, CURRENCY_DOLLAR, CURRENCY_CENT])

    # Add common energy price units (currency per energy)
    # These are not predefined in HA but are commonly used for electricity pricing
    energy_units = ["Wh", "kWh", "MWh"]
    units.extend(
        f"{currency}/{energy}"
        for currency in [CURRENCY_EURO, CURRENCY_DOLLAR, CURRENCY_CENT]
        for energy in energy_units
    )

    return sorted(set(units))


def detect_value_type_and_suggestions(value: Any) -> dict[str, Any]:
    """
    Detect the type of a value and suggest appropriate configuration.

    Args:
        value: The value to analyze.

    Returns:
        Dictionary with suggested value_type, unit_of_measurement, and device_class.
    """
    suggestions: dict[str, Any] = {
        "value_type": VALUE_TYPE_STRING,
        "unit_of_measurement": "",
        "device_class": "",
    }

    if value is None:
        return suggestions

    if isinstance(value, bool):
        suggestions["value_type"] = VALUE_TYPE_BOOLEAN
        return suggestions

    if isinstance(value, int | float):
        suggestions["value_type"] = VALUE_TYPE_NUMBER
        # Could add heuristics here based on value range or field name
        return suggestions

    if isinstance(value, str):
        # Try to detect timestamp patterns (ISO 8601)
        iso_pattern = r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
        if re.match(iso_pattern, value):
            suggestions["value_type"] = VALUE_TYPE_TIMESTAMP
            suggestions["device_class"] = "timestamp"
        return suggestions

    # Default to string for unknown types
    return suggestions
