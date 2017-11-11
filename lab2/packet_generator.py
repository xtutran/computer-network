import random, sys
from socket import *


hostsA = ['192.168.128.7', '192.168.128.1']
hostsC = ['192.224.0.5', '192.224.0.7', '192.224.10.5', '192.224.15.6']


def gen_packets(packet_num=5):
    packets = []
    for i in range(0, packet_num):
        packet_id = i
        source = random.choice(hostsA)
        destination = random.choice(hostsC)
        ttl = random.randint(1, 4)
        packets.append('%d, %s, %s, %d, testing' % (packet_id, source, destination, ttl))

    print packets


# main method to launch the client
def main():
    argv = sys.argv
    if len(argv) != 2:
        print 'Usage: python packet_generator.py <router port>'
        sys.exit(1)

    if not argv[1].isdigit():
        print 'Port must be a number'
        sys.exit(1)

    port = int(argv[1])
    # create a client socket and connect to server
    clientsock = socket(AF_INET, SOCK_DGRAM)  # Create a socket object
    print 'Open a connection'
    clientsock.connect(('127.0.0.1', port))
    i = 0
    try:
        while True:
            packet_id = i
            source = random.choice(hostsA)
            destination = random.choice(hostsC)
            ttl = random.randint(1, 4)
            packet = '%d, %s, %s, %d, testing' % (packet_id, source, destination, ttl)
            print 'sent ' + packet
            clientsock.send(packet)
            i += 1
    except KeyboardInterrupt as err:
        print 'Warning: terminated by user'
        clientsock.send('$')
        sys.exit(1)


if __name__ == "__main__":
    main()
