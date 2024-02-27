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
service: awtrix.push_app_data
data: 
  device: awtrix_bedroom
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
service: awtrix.push_app_data
data: 
  device: awtrix_bedroom
  name: test
  data: 
```

ver 20240226.01

# Change Settings

```
service: awtrix.settings
data:
  device: awtrix_bedroom
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
data:
  device: awtrix_bedroom
  name: Time    
```