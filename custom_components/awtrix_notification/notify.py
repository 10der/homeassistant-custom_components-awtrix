"""Support for Awtrix notifications."""

import json
import logging

from homeassistant.components.notify import ATTR_DATA, BaseNotificationService

from .const import CONF_DEVICE

_LOGGER = logging.getLogger(__name__)

async def async_get_service(hass, config, discovery_info=None):
    """Get the Awtrix notification service."""

    if discovery_info is None:
        return None

    entity_id =  discovery_info[CONF_DEVICE]
    return AwtrixNotificationService(entity_id)


########################################################################################################

class AwtrixNotificationService(BaseNotificationService):
    """Implement the notification service for Awtric."""

    def __init__(self, entity_id):
        """Init the notification service for Awtric."""
        self.entity_id = entity_id


    async def notification(self, topic, message, data):
        """Handle the notification service for Awtric."""

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
