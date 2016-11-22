import dht
import machine

d = dht.DHT11(machine.Pin(2))

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body>
        <h1>The current temperature is: <small>%s</small></h1>
        <h1>The current humidity is: <small>%s</small></h1>
    </body>
</html>
"""

import socket

def main():

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html % (temperature,humidity)
        cl.send(response)
        cl.close()

main()
