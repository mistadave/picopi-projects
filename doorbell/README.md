# Doorbell project

This door bell works with the [Shelly Door Window 2](https://kb.shelly.cloud/knowledge-base/shelly-door-window-2).

The idea behind this project was, that a door bell rings in an other room, than the actual door is located at. You will get some kind of noice alert (Door ring) which indicates, that the door whas openend by a magnet switch on the door itself, in this case the Shelly Door/Window 2 sensor.

The problem actually is, that bluetooth or direct wifi connection from sender (door sensor) and receive (this door bell) wan't work because of the range.

The solution was to use a mqtt broker in the middle to transtport the message from the door to the bell. Also was the decion to use a mqtt borker shelly's existing integration for mqtt.

Now the door bell device just needs to subscribe to the right topic from the shelly device and act on the incomming messege.


## Requirements

- [Raspberry Pi Pico W/WH](https://www.pi-shop.ch/raspberry-pi-pico-wh)
- [Audio Expansion Module for Raspberry Pi Pico](https://www.pi-shop.ch/audio-expansion-module-for-raspberry-pi-pico)
- [Shellydw2](https://kb.shelly.cloud/knowledge-base/shelly-door-window-2)
    [Brack Shop](https://www.brack.ch/shelly-wlan-tuer-fensterkontakt-door-window-2-983980)
- MQTT broker (for example [mosquitto](https://mosquitto.org))

Link to tutorial with Pico Pi. [Getting Started](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2)

## Configuration

With [Thonny IDE](https://thonny.org) make the following settings.

- Go to **tools > options...> Interpreter** and set the interpreter to `CircuitPython(Generic)`
- **tools > manage plugins** and search for `adafruit-circuitpython-minimqtt`. Install the plugin

change the following variables in `doorbell.py` according to your needs.

```python
WLAN_SSID = 'my-ssid'   # replace with your SSID
WLAN_PW = 'my-wifi-password.'   # replace with your pw
MQTT_BROKER = 'mqtt-broker' # replace with mqtt broker address (ip, dns)
MQTT_ID = 'pico_pi_door_bell' # optional, set own id
MQTT_USER = ''
MQTT_PW = ''
topic = "shellies/shellydw2-myshellyid/sensor/state" # replace myshellyid
```

Copy the doorbell.py and dingdong.wav file onto the Pico Pi W.
