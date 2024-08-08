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

ver 20240310.03

experimental!
create weather application

```
service: awtrix.awtrix_bedroom_weather_app
data:
 weather: weather.forecast_home
 outside_temperature: sensor.easyweatherv1_6_4_outdoor_temperature
 home_temperature: sensor.home_temperature
 moon: sensor.moon_phase
 sun: sun.sun
```

- no need to upload icons
- able to customize icons

```
service: awtrix.awtrix_bedroom_weather_app
data:
  weather: weather.forecast_home
  outside_temperature: sensor.easyweatherv1_6_4_outdoor_temperature
  home_temperature: sensor.home_temperature
  sun: sun.sun
  moon: sensor.moon_phase
  icons:
      clear-night: "a12181" 
      cloudy: "a2283"
      exceptional: "a2364"
      fog: "17056"
      hail: "a2441" 
      lightning: "a630" 
      lightning-rainy: "a49299" 
      partlycloudy: "a2286" 
      pouring: "a49300" 
      rainy: "a2284" 
      snowy: "a2289" 
      snowy-rainy: "a49301" 
      sunny: "a2282" 
      windy: "a15618" 
      windy-variant: "a15618" 
      full_moon: "2314" 
      waning_gibbous: "2315" 
      last_quarter: "2316" 
      waning_crescent: "2317" 
      new_moon: "2318"
      waxing_crescent: "2320" 
      first_quarter: "2320" 
      waxing_gibbous: "36234" 
      home:  "96"
      sunrise: "485" 
      sunset: "486" 
      unavailable:  "52176"
```

ver 20240311.01
bug fixes

ver 20240317.01
able to configure apps

```
service: awtrix.awtrix_bedroom_weather_app
data:
  weather: weather.forecast_home
  outside_temperature: sensor.easyweatherv1_6_4_outdoor_temperature
  home_temperature: sensor.home_temperature
  sun: sun.sun
  moon: sensor.moon_phase
  data:
    sun_event_minute_threshold: 180
    weather_sun:
      rainbow: true
      repeat: 3
      duration: 10
```

app names 
weather, weather_night, weather_sun, weather_home

ver 20240318.01
bugfix


ver 20240320.01

```
service: awtrix.awtrix_bedroom_rtttl
data: 
 rtttl: "two_short:d=4,o=5,b=100:16e6,16e6"
```

```
service: awtrix.awtrix_bedroom_sound
data:
 sound: beep
```

Hold notification
```
service: notify.awtrix_bedroom
data:
  message: "Hello!"
  data: 
    hold: true
```

Dismiss hold notification
```
service: notify.awtrix_bedroom
data:
  message: ""
```

ver 20240328.01
able to add weather custom pages

```
service: awtrix.awtrix_bedroom_weather_app
data:
  weather: weather.forecast_home
  outside_temperature: sensor.easyweatherv1_6_4_outdoor_temperature
  home_temperature: sensor.home_temperature
  sun: sun.sun
  moon: sensor.moon_phase
  frames:
    wind: 
      icon: "2298"
      text: "{{ states('sensor.easyweatherv1_6_4_wind_gust') }} km/h "
```

simaple automation

```
alias: bathroom current temperature
description: bathroom current temperature
trigger:
  - platform: time_pattern
    minutes: /5
condition: []
action:
  - service: awtrix.awtrix_bedroom_push_app_data
    data:
      name: home_temperature
      data:
        text: "{{states('sensor.bathroom_current_temperature')}}°"
        icon: "2056"
        duration: 5
        pushIcon: 2
        lifetime: 900
        repeat: 1
mode: single
```