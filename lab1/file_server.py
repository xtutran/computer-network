from socket import *
import os, os.path
import datetime
import logging
import sys


# main method to launch the server
def main():
    argv = sys.argv
    if len(argv) != 4:
        print 'Usage: python file_server.py 9090 /some/where/documents /some/where/logfile'
        sys.exit(1)

    if not argv[1].isdigit():
        print 'Port must be a number'
        sys.exit(1)

    port = int(argv[1])  # Reserve a port for your service.
    host = '127.0.0.1'
    folder = argv[2]
    logging.basicConfig(filename=argv[3], format='%(message)s', filemode='w', level=logging.INFO)
    serversocket = socket(AF_INET, SOCK_DGRAM)  # Create a socket object
    serversocket.bind((host, port))  # Bind to the port
    serversocket.setblocking(True)

    # Now wait for client connection.
    print 'Server listening....'
    while True:
        try:
            packet_bytes, recv_addr = serversocket.recvfrom(1024)
            if packet_bytes:
                request_file = str.encode(packet_bytes)
                recv_time = datetime.datetime.now()
                request_path = folder + '/' + request_file
                # this works on Linux only
                if os.fork() == 0:
                    # Child Process
                    request_handler(recv_time, request_path, serversocket, recv_addr)
                else:
                    continue
        except:
            sys.exit(1)


# process client request
def request_handler(recv_time, request_path, sock, recv_addr):
    print 'Processing file request: %s from %s' % (request_path, recv_addr)
    status_mssg = 'file not found'
    if os.path.isfile(request_path) and os.access(request_path, os.R_OK):
        # do something
        try:
            f = open(request_path, 'rb')
            # split file by chunk 1mb
            l = f.read(1024)
            i = 0
            while l:
                sock.sendto(l, recv_addr)
                # print('Sent ', repr(l))
                l = f.read(1024)
                i += 1
            f.close()
            if i >= 2:
                sock.sendto("$", recv_addr)
            # flag = True
            status_mssg = datetime.datetime.now()
        except:
            status_mssg = 'transmission not completed'
        print 'Done'
    else:
        print status_mssg
    # construct log message
    mssg = '<%s> <%s> <%s> <%s> <%s>' % \
          (recv_addr[0], recv_addr[1], os.path.basename(request_path), recv_time, status_mssg)
    logging.info(mssg)


if __name__ == "__main__":
    main()
