#!usr/bin/env python3

from time import sleep
from opcua import Server

server = Server()
server.set_endpoint("opc.tcp://192.168.113.38:3300")
server.register_namespace("Digital Twin HORST600")

objects = server.get_objects_node()

temp_sensor = objects.add_object('ns=2;s="tempsens"', "Temperatursensor")
temperature = temp_sensor.add_variable('ns=2;s="temp"', "Aktuelle Temperatur", 0)
temperature.set_writable()

shock_sensor = objects.add_object('ns=2;s="tempsens"', "Temperatursensor")
shock_detected = temp_sensor.add_variable('ns=2;s="temp"', "Aktuelle Temperatur", False)
shock_detected.set_writable()



try:
    print("Start Server")
    server.start()
    print("Server Online")
    while True:
        print(f"""Aktuelle Temperatur: {temperature.get_value()}
                  Erschuetterung erkannt: {shock_detected.get_value()}""")
        sleep(2)
finally:
    server.stop()
    print("Server offline")