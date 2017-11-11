#!/usr/bin/env python
import socket  # Import socket module
import sys

# Read environment arguments
argv = sys.argv
if len(argv) != 4:
    print 'Usage: python edmts_client.py <server ip> <port> <temperature unit>'
    sys.exit(1)

if not argv[2].isdigit():
    print 'Port must be a number'
    sys.exit(1)

host = argv[1]
port = int(argv[2])
request = argv[3]

try:
    # Connect to the socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a tcp socket object
    s.connect((host, port))
    # Send a request
    s.send(request)
    data = ''
    while True:
        more = s.recv(1024)
        if not more:
            break
        data += more
    # Output the response
    print repr(data)
    s.close()
except socket.error as err:
    print 'Error: unable to connect to the server at', host, port
    sys.exit(1)