import time
import board
import adafruit_dht
from datetime import datetime, timedelta
import pandas as pd

# Initialize the dht device with the data pin connected to pin 16 (GPIO 23) of the Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D14)

# You can pass DHT22 use_pulseio=False if you do not want to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

timestamps = []
datalist = []

full_run = time.time() + 60*3 

while time.time() < full_run:
    starttime = datetime.now()
    print(starttime)
    try:
        # Print the values via the serial interface
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        timestamps.append(starttime.strftime("%H:%M:%S"))
        datalist.append([temperature_c, humidity])

    except RuntimeError as error:
        # Errors happen quite often, DHT's are hard to read, just move on
        print(error.args[0])
        datalist.append(['error', 'error'])
        timestamps.append(starttime.strftime("%H:%M:%S"))
        endtime = datetime.now()
        time_used = endtime - starttime
        time.sleep(2.0-time_used.total_seconds())
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    endtime = datetime.now()
    time_used = endtime - starttime
    time.sleep(2.0-time_used.total_seconds())

df=pd.DataFrame(datalist, index=timestamps, columns=['Temperature [C]', 'Humitity'])

df.to_excel("/home/cornelia/Documents/Sensortests_1/Data/015_temp_hum.xlsx")
    