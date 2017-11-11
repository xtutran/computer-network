#!/usr/bin/env python
import socket
import sys
import datetime
import random


def gen_celsius_temperature():
    return random.randint(-30, 40)


def celsius_to_fahrenheit(temp):
    return temp * 9/5 + 32

# Read environment arguments
argv = sys.argv
if len(argv) != 2:
    print 'Usage: python edmts_server.py <port>'
    sys.exit(1)

if not argv[1].isdigit():
    print 'Port must be a number'
    sys.exit(1)
port = int(argv[1])
host = socket.gethostname()  # Get local machine name
host = socket.gethostbyname(socket.gethostname())
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a tcp socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print 'EDMTS is running on', host, ', listening on port', port

    reply_format = 'Edmonton is at %d %s at %s'
    while True:
        conn, recv_addr = s.accept()  # Establish connection with client.
        print 'Got connection from', recv_addr

        data = conn.recv(1024)
        print 'Response the request...'

        recv_time = datetime.datetime.now().strftime('%a %b %-m %H:%M:%S %Y')
        reply_mssg = 'Wrong format request. The request should be Fahrenheit or Celsius'
        if data.lower() == 'fahrenheit':
            temperature = celsius_to_fahrenheit(gen_celsius_temperature())
            reply_mssg = reply_format % (temperature, data, str(recv_time))
        elif data.lower() == 'celsius':
            temperature = gen_celsius_temperature()
            reply_mssg = reply_format % (temperature, data, str(recv_time))
        conn.send(reply_mssg)
        conn.close()
        print('Done sending')
except socket.error as err:
    print 'Error: unable to listen to the specified TCP port: ' + str(port)
    sys.exit(1)
except KeyboardInterrupt as e:
    print 'Terminated by user!'
    sys.exit(1)
