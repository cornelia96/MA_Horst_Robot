from time import sleep
from threading import Thread

def start_server():
    import server

def start_temp():
    import tempsens_client

def start_shock():
    import shock_client


thread_server = Thread(target = start_server)
thread_temp = Thread(target = start_temp)
thread_shock = Thread(target = start_shock)

thread_server.start()
thread_temp.start()
thread_shock.start()

thread_server.join()
thread_temp.join()
thread_shock.join()