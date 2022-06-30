import socket

ip_address = socket.gethostbyname(socket.gethostname() + ".local")

tempsens_pin = 14 
shocksens_pin = 15