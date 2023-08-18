import os
import ipaddress
import wifi
import socketpool
import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import audiocore
import audiobusio
import digitalio

WLAN_SSID = 'my-ssid'
WLAN_PW = 'my-wifi-password.'
MQTT_BROKER = 'mqtt-broker'
MQTT_ID = 'pico_pi_door_bell'
MQTT_USER = ''
MQTT_PW = ''
topic = "shellies/shellydw2-myshellyid/sensor/state"
status_topic = 'device/doorbell/status'

# init speaker
audio = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)

# init WIFI
wifi.radio.connect(WLAN_SSID, WLAN_PW)
print(f"Connected to WiFi: {WLAN_SSID}")
pool = socketpool.SocketPool(wifi.radio)

def play_melody():
    # Play your sound
    f = open("sounds/dingdong.wav", "rb")
    wav = audiocore.WaveFile(f)
    audio.play(wav)
    while audio.playing:
      pass

def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def on_door_msg(client, topic, message):
    # print("Door status: {}".format(message))
    if message == "open":
        play_melody()



def on_message(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))


print("connect to mqtt broker")
client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=1883,
    username=MQTT_USER,
    password=MQTT_PW,
    socket_pool=pool
    #ssl_context=ssl.create_default_context(),
)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.on_unsubscribe = unsubscribe
client.on_message = on_message
client.add_topic_callback(
    topic, on_door_msg
)

client.will_set(status_topic,'Goodbye')

print("Connecting to MQTT broker...")
client.connect()

print("Publishing to %s" % status_topic)
client.publish(status_topic, "Hello")

# Subscribe to all notifications on the device group
client.subscribe(topic, 0)

while True:
    try:
        client.loop()
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        client.reconnect()
        client.subscribe(topic, 0)
        continue
    time.sleep(1)

