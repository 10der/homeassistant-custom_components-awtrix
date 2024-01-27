# homeassistant-custom_components-awtrix
HASS awtrix 

just add to
# configuration.yaml 

```
awtrix:
```

# example

```
service: notify.awtrix_bedroom
data:
  message: The garage door has been open for 10 minutes.
```

or extend format
```
service: notify.awtrix_bedroom
data:
  message: The garage door has been open for 10 minutes.
  data:
    icon: "33655"
    sound: beep
```
