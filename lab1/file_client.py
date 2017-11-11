from socket import *  # Import socket module
import sys


# main method to launch the client
def main():
    argv = sys.argv
    if len(argv) != 4:
        print 'Usage: python file_client.py 192.168.10.1 9090 filename'
        sys.exit(1)

    if not argv[2].isdigit():
        print 'Port must be a number'
        sys.exit(1)
    host = argv[1]
    port = int(argv[2])  # Reserve a port for your service.
    request_file = argv[3]

    # create a client socket and connect to server
    clientsock = socket(AF_INET, SOCK_DGRAM)  # Create a socket object
    print 'Open a connection'
    clientsock.connect((host, port))
    print 'Request a file: %s' % (request_file)
    clientsock.send(request_file)

    with open(request_file, 'wb') as f:
        while True:
            # wait response from server in 5 seconds
            clientsock.settimeout(5)
            try:
                data = clientsock.recv(1024)

                if len(data) < 1024 or data == '$':
                    break

                if not data:
                    break
                f.write(data)
            except timeout:
                print 'the transmission had been aborted'
                sys.exit(1)
            except error:
                print 'connection refuse'

    print 'Successfully get the file'
    f.close()
    print 'Connection closed'
    clientsock.close()


if __name__ == "__main__":
    main()
