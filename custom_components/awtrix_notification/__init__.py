"""Support for Awtrix time."""

from __future__ import annotations

import logging

from homeassistant.const import CONF_NAME, Platform
from homeassistant.helpers import (
    device_registry as dr,
    discovery,
    entity_registry as er,
)

from .const import CONF_DEVICE, DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Awtrix."""

    devices = []

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    for device in device_registry.devices.values():
        ha_device_name = device.name_by_user or device.name
        if device.manufacturer == 'Blueforcer':

            device_entities = er.async_entries_for_device(
                entity_registry,
                device_id=device.id,
                include_disabled_entities=False,
            )

            for entry in device_entities:
                if 'device_topic' in entry.entity_id:
                    devices.append({CONF_NAME: ha_device_name,
                                   CONF_DEVICE: entry.entity_id})

    for device_conf in devices:
        hass.async_create_task(
            discovery.async_load_platform(
                hass, Platform.NOTIFY, DOMAIN, device_conf, config)
        )

    # Return boolean to indicate that initialization was successfully.
    return True
