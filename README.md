# homeassistant-custom_components-awtrix
HASS awtrix 

just add to
# configuration.yaml 

```
awtrix:
```

ver 20240128.03

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

ver 20240209.01

# Create a custom app

```
service: awtrix.awtrix_bedroom_push_app_data
data: 
  name: test
  data:
    text : "Hello, AWTRIX Light!"
    rainbow: true
    icon: "87"
    duration: 5
    pushIcon: 2
    lifetime: 900
    repeat: 1
```

# Remove app

```
service: awtrix.awtrix_bedroom_push_app_data
data: 
  name: test
```

ver 20240226.01

# Change Settings

```
service: awtrix.awtrix_bedroom_settings
data:
    WD: false 
    TIME_COL: 
      - 255
      - 0
      - 0
    TMODE: 0 
    BRI: 1
    ABRI: false
    ATRANS: false
```

# Switch to App name

```
service: awtrix.awtrix_bedroom_switch_app
data: 
  name: Time
```

# back

```
service: awtrix.awtrix_bedroom_settings
data:
    WD: true 
    TIME_COL: 
      - 255
      - 255
      - 255
    TMODE: 1 
    BRI: 1
    ABRI: true
    ATRANS: true
```

ver 20240301.01

added service description
