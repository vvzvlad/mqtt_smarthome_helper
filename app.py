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
from locale import atof, setlocale, LC_NUMERIC

import os
import json
import sys
import random

room_temp = 0
local_temp = 0
local_temp_cal = 0
local_temp_cal_calc = 0

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("zigbee/sensor_082a")
  client.subscribe("zigbee/thermostat_0403")
  client.publish("mqtt_helper/status", payload="mqtt helper daemon started", qos=0, retain=False)
  client.publish("zigbee/thermostat_0403/set", str("{\"eco_temperature\": 25}"), qos=0, retain=False)


def on_message(client, userdata, msg):
  #print("Received MQTT message:" + msg.topic + ": " + str(msg.payload))
  global room_temp, local_temp, local_temp_cal, local_temp_cal_calc

  if msg.topic == "zigbee/sensor_082a":
    json_data = json.loads(msg.payload)
    room_temp = json_data.get('temperature')
    print("temperature: " + str(room_temp))
  if msg.topic == "zigbee/thermostat_0403":
    json_data = json.loads(msg.payload)
    local_temp = json_data.get('local_temperature')
    local_temp_cal = json_data.get('local_temperature_calibration')
    print("local temperature: " + str(local_temp) + ", cal: " + str(local_temp_cal))



def main():
  counter = 0
  period = 60
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect("192.168.88.111", 1883, 60)
  time.sleep(5)
  client.loop_start()
  while True:
    time.sleep(period)
    uptime = counter * period
    counter = counter + 1
    client.publish("mqtt_helper/status/uptime", str(uptime), qos=0, retain=False)

    if room_temp != 0 and local_temp != 0:
      current_local_temp_cal_calc = round(room_temp-local_temp, 1) + local_temp_cal
      current_local_temp_cal_calc = str(current_local_temp_cal_calc)
      print("current calc cal: " + current_local_temp_cal_calc + ", calc cal: " + str(round(room_temp-local_temp, 1)) + ", old cal: " + str(local_temp_cal) + ", local: " + str(local_temp) + ", room: " + str(room_temp))

      client.publish("zigbee/thermostat_0403/set", str("{\"local_temperature_calibration\": " + current_local_temp_cal_calc + "}"), qos=0, retain=False)

  client.loop_stop()



if __name__ == "__main__":
  main()
