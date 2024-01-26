# homeassistant-custom_components-awtrix
HASS awtrix 

# notify.yaml

```
- name: awtrix_bedroom
  platform: awtrix
  device: awtrix_7c43d4

- name: awtrix_hall
  platform: awtrix
  device: awtrix_diy
```

<img alt='Hass awtrix entity' src='hass-config.png'/>

# example

```
service: notify.awtrix_bedroom
data:
  message: The garage door has been open for 10 minutes.
  title: Your Garage Door Friend
  target: platform specific
  data:
    icon: "33655"
    sound: beep
```

