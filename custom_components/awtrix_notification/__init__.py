"""Support for Awtrix time."""

from __future__ import annotations

import logging

from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import ServiceCall, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import (
    device_registry as dr,
    discovery,
    entity_registry as er,
)

from .awtrix import AwtrixTime
from .const import CONF_DEVICE, DATA_CONFIG_ENTRIES, DOMAIN

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

    hass.data[DOMAIN] = {
        DATA_CONFIG_ENTRIES: devices
    }

    for device_conf in devices:
        hass.async_create_task(
            discovery.async_load_platform(
                hass, Platform.NOTIFY, DOMAIN, device_conf, config)
        )

    def find_enity(name):
        """Find entity by name."""

        device = None
        for device_conf in hass.data[DOMAIN][DATA_CONFIG_ENTRIES]:
            if device_conf['name'] == name:
                device = AwtrixTime(hass, device_conf[CONF_DEVICE])
        if device:
            return device
        else:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="invalid_device",
                translation_placeholders={
                    "target": name, "domain": DOMAIN},
            )

    """Set up the an async service example component."""
    @callback
    def push_appdata_service(call: ServiceCall) -> None:
        """AWTRIX app service."""

        device = find_enity(call.data['device'])
        hass.loop.create_task(device.push(
            call.data['name'], call.data['data']))

    @callback
    def call_settings_service(call: ServiceCall) -> None:
        """AWTRIX app setting service."""

        device = find_enity(call.data['device'])
        hass.loop.create_task(device.settings(
            call.data['data']))

    @callback
    def call_switch_app_service(call: ServiceCall) -> None:
        """AWTRIX app switch service."""

        device = find_enity(call.data['device'])
        hass.loop.create_task(device.switch_app(
            call.data['name']))

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, 'push_app_data', push_appdata_service)
    hass.services.async_register(DOMAIN, 'settings', call_settings_service)
    hass.services.async_register(DOMAIN, 'switch_app', call_switch_app_service)

    # Return boolean to indicate that initialization was successfully.
    return True
