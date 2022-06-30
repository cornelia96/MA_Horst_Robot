#!usr/bin/env python3

from opcua import Client
import glob
import RPi.GPIO as GPIO
from time import sleep
import constants


client = Client(f"opc.tcp://{constants.ip_address}:3300")
client.connect()

client.get_namespace_array()

objects = client.get_objects_node()

shocksensor = objects.get_children()[2]

shock_detected = shocksensor.get_children()[0]

print("client started")