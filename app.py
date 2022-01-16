#!/usr/bin/env -S python3 -u

#
#############################################################################
#
# helper to mqtt for smarthome
#
#############################################################################
#

import paho.mqtt.client as mqtt
import time

import os
import json
import sys
import random

value = 0

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  #client.subscribe("mqtt_helper/wakeup")
  client.publish("mqtt_helper/status", payload="mqtt helper daemon started", qos=0, retain=False)


def on_message(client, userdata, msg):
  print("Received MQTT message:" + msg.topic + ": " + str(msg.payload))

  if msg.topic == "mqtt_helper/wakeup":
    json_data = json.loads(msg.payload)
    playlist_name = json_data.get('playlist')
    device_name = json_data.get('device')
    if playlist_name is not None and device_name is not None:
      check_play_and_start_playlist(playlist_name, device_name)



def main():
  counter = 0
  period = 10*60
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect("192.168.88.111", 1883, 60)
  time.sleep(5)
  client.loop_start()
  while True:
    uptime = counter * period
    client.publish("mqtt_helper/status/uptime", str(uptime), qos=0, retain=False)
    client.publish("zigbee/thermostat_0403/set", str("{\"eco_temperature\": 17}"), qos=0, retain=False)
    time.sleep(period)
    counter = counter + 1
  client.loop_stop()



if __name__ == "__main__":
  main()
