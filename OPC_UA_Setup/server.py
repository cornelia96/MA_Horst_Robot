#!usr/bin/env python3

from time import sleep
from opcua import Server
import constants
from threading import Thread

def start_temp():
    import tempsens_client

def start_shock():
    import shock_client

def start_tilt():
    import tiltsens_client

threads = [Thread(target = start_temp), Thread(target = start_shock), Thread(target = start_tilt)]

server = Server()
server.set_endpoint(f"opc.tcp://{constants.ip_address}:3300")
server.register_namespace("Digital Twin HORST600")

objects = server.get_objects_node()

temp_sensor = objects.add_object('ns=2;s="tempsens"', "Temperatursensor")
temperature = temp_sensor.add_variable('ns=2;s="temp"', "Aktuelle Temperatur", 0)
temperature.set_writable()

shock_sensor = objects.add_object('ns=2;s="shocksens"', "Erschuetterungsschalter")
shock_detected = shock_sensor.add_variable('ns=2;s="shock"', "Erschuetterung detektiert", False)
shock_detected.set_writable()

tilt_sensor = objects.add_object('ns=2;s="tiltsens"', "Neigungsschalter")
tilt_detected = tilt_sensor.add_variable('ns=2;s="tilt"', "Neigung detektiert", False)
tilt_detected.set_writable()

try:
    print("Start Server")
    server.start()
    print("Server Online")

    for td in threads:
        td.start()

    while True:
        print(f"""Aktuelle Temperatur: {temperature.get_value()}
                  Erschuetterung erkannt: {shock_detected.get_value()}
                  Neigung erkannt: {tilt_detected.get_value()}""")
        sleep(0.5)
        
except KeyboardInterrupt:
    for td in threads:
        td.join()
    server.stop()
    print("Server offline")


