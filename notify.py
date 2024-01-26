# -*- coding: utf-8 -*-

"""Support for Awtrix notifications."""

import logging
import json

from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,
)

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    BaseNotificationService,
)

CONF_DEVICE = "device"

_LOGGER = logging.getLogger(__name__)

def get_awtrix_entity(hass, device_name):

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
  
    for device in device_registry.devices.values():
        ha_device_name = device.name_by_user or device.name
        if device.manufacturer == 'Blueforcer' and ha_device_name == device_name:

           device_entities = er.async_entries_for_device(
               entity_registry,
               device_id=device.id,
               include_disabled_entities=False,
           )

           for entry in device_entities:
               if 'device_topic' in entry.entity_id:
                  return entry.entity_id

async def async_get_service(hass, config, discovery_info=None):
    """Get the Awtrix notification service."""

    device_name = config[CONF_DEVICE]
    # _LOGGER.warning("AWTRIX NOTIFICATION DEVICE: %s", device_name)
 
    entity_id = get_awtrix_entity(hass, device_name.strip())
    if entity_id is not None:
       return AwtrixNotificationService(entity_id)



########################################################################################################

class AwtrixNotificationService(BaseNotificationService):

    """Implement the notification service for Awtric."""

    def __init__(self, entity_id):
        self.entity_id = entity_id


    async def notification(self, topic, message, data):
        icon = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAAIAAgDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACP/EAB8QAAECBgMAAAAAAAAAAAAAABgWFwAIFBUZKAclN//EABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwAIsRKxgUyFXyX80lq0bFEZx0Oow1CqANlHPTviW2NBfMjhh7BPgVvZwH//2Q=="
        rtttl = "Notification:d=2,o=4,b=160:32g,32p,32g,32p,32g,32p"

        data = data or {"icon" : icon, "rtttl" : rtttl }
        msg = data.copy()
        msg["text"] = message

        #"""Service to send a message."""
        payload = json.dumps(msg)
        service_data = {"payload_template": payload,
                        "topic": topic + "/notify"}

        return await self.hass.services.async_call(
            "mqtt", "publish", service_data
        )

    async def async_send_message(self, message='', **kwargs):
        """Send a message to some Awtrix device."""

        state = self.hass.states.get(self.entity_id)
        if state is not None and state.state is not None:
           topic = state.state
           data = kwargs.get(ATTR_DATA)
           await self.notification(topic, message, data)
