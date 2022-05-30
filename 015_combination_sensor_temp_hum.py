import time
import board
import adafruit_dht

# Initialize the dht device with the data pin connected to pin 16 (GPIO 23) of the Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D23)

# You can pass DHT22 use_pulseio=False if you do not want to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values via the serial interface
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

    except RuntimeError as error:
        # Errors happen quite often, DHT's are hard to read, just move on
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
    